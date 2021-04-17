import os

import MySQLdb
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Manager
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator

from .models import User, Announcement

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

class UserView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    login_url = '/'
    redirect_field_name = None

    def test_func(self):
        return not self.request.user.is_blocked


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # TEMPORARY SOLUTION: Log out then quit to home page
        logout(request)
        return super(HomePageView, self).get(request, *args, **kwargs)

    def post(self, request, **kwargs):
        form_type = request.POST.get('form_type')
        context = self.get_context_data(**kwargs)

        # Login form handler
        if form_type == 'login':
            login_username = request.POST.get('login_username')
            login_password = request.POST.get('login_password')

            user = authenticate(username=login_username, password=login_password)

            if user is None:
                context['user_not_exists'] = True
                return render(request, "index.html", context)
            else:
                login(request, user)
                context['user_not_exists'] = False
                if user.is_superuser:
                    return redirect('/admin/account')
                else:
                    return redirect('/user/account')

        # Registration form handler
        elif form_type == 'registration':
            register_email = request.POST.get('register_email')
            register_name = request.POST.get('register_name')
            register_pass = request.POST.get('register_pass')
            register_pass2 = request.POST.get('register_pass2')

            try:
                if register_pass != register_pass2:
                    # user registration was unsuccessful
                    # so we need to say this to him

                    context['pass_not_match'] = True

                    return render(request, "index.html", context)
                else:
                    user = User.objects.create_user(
                        username=register_name,
                        email=register_email,
                        password=register_pass,
                        is_active=False,
                    )

                    current_site = get_current_site(request)
                    mail_subject = 'Activate your account.'

                    # Create message using template acc_active_email.html
                    message = render_to_string('acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                    })
                    to_email = register_email
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                    return HttpResponse('Please confirm your email address to complete the registration')
              
            except ValidationError:
                # Username, email or password are not allowed
                context['registration_failed'] = True
                return render(request, "index.html", context)
            except Exception as e:
                print('ERROR:', str(e))
                # user registration was unsuccessful
                # so we need to say this to him

                # Check if user with specified email exists
                try:
                    user = User.objects.get(email=register_email)
                    context['registration_email_exists'] = True
                except:
                    # If user with specified email not exists
                    # check for specified username
                    try:
                        user = User.objects.get(username=register_name)
                        context['registration_login_exists'] = True
                    except Exception as e:
                        print('ERROR:', str(e))
                        # If in this branch reason of creating user is unknown
                        context['registration_error_unknown'] = True

                return render(request, "index.html", context)
        else:
            return redirect('/')


class AccountView(UserView):
    template_name = 'user/account.html'


class AddAnnouncementView(UserView):
    template_name = 'user/create.html'

    def post(self, request: WSGIRequest, **kwargs):
        data = {
            'name': request.POST.get('name'),
            'type': request.POST.get('type')[0],
            'sex': request.POST.get('sex')[0],
            'photo_id': request.POST.get('photo_id'),  # TODO: Image saving (now it`s just user`s file name)
            'paws_number': request.POST.get('paws_number'),
            'ears_number': request.POST.get('ears_number'),
            'has_tail': request.POST.get('has_tail')[0],
            'description': request.POST.get('description'),
            'last_seen_timestamp': request.POST.get('last_seen_timestamp'),
            'last_seen_point_lat': request.POST.get('last_seen_point_lat'),
            'last_seen_point_lng': request.POST.get('last_seen_point_lng'),
            'user_obj': request.user
        }

        # TODO: Error handling
        try:
            ann = Announcement.objects.create(**data)
            ann.save()
        except Exception as e:
            print('ERROR:', str(e))
            return redirect('/')

        return redirect('/user/create')


class AddEditAnnouncementHandler(UserView):
    template_name = 'user/create.html'

class MapView(UserView):
    template_name = 'user/map.html'

class PetView(UserView):
    template_name = 'user/pet.html'

def index(request):
    info = 'MySQL Server Version: '

    if os.getenv('GAE_APPLICATION', None):
        # Running on production App Engine, so connect to Google Cloud SQL using
        # the unix socket at /cloudsql/<your-cloudsql-connection string>
        db = MySQLdb.connect(
            unix_socket=settings.DATABASES['default']['HOST'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            database=settings.DATABASES['default']['NAME']
        )
    else:
        # Running locally so connect to either a local MySQL instance or connect to
        # Cloud SQL via the proxy.
        db = MySQLdb.connect(
            host=settings.DATABASES['default']['HOST'],
            port=int(settings.DATABASES['default']['PORT']),
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            database=settings.DATABASES['default']['NAME']
        )

    cursor = db.cursor()
    cursor.execute("select version()")

    data = cursor.fetchone()
    info += str(data)

    info = '<h1>' + info + '</h1>'
    db.close()
    return HttpResponse(info)

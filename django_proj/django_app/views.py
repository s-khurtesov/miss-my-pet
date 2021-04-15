import os

import MySQLdb
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Manager
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .models import User, Announcement


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        # context['user_not_exists'] = False
        # This variable is used to show user that registration attempt was failed due to some reason
        # context['registration_failed'] = False
        # This variable is used to show user 'Registration success' from and send email to his email
        # context['registration_succeed'] = False
        # context['pass_not_match'] = False
        return context

    def get(self, request, *args, **kwargs):
        # TEMPORARU SOLUTION: Log out then quit to home page
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
                    return redirect('/admin/account/')
                else:
                    return redirect('/user/account/' + user.username)

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
                        password=register_pass
                    )
                    login(request, user)

                    # if user registration successful then say this to him
                    # and redirect him to his new account

                    # TODO: Maybe we shouldn't let user enter to his account until he confirms email?
                    return redirect('/user/account/' + register_name)
            except ValidationError:
                # Username, email or password are not allowed
                context['registration_failed'] = True
                return render(request, "index.html", context)
            except:
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
            return redirect('/user/account/dump_motherfucker')


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'user/account.html'
    login_url = '/'
    redirect_field_name = None


class AddAnnouncementView(LoginRequiredMixin, TemplateView):
    template_name = 'user/create.html'
    login_url = '/'
    redirect_field_name = None

    def post(self, request: WSGIRequest, **kwargs):
        # context = self.get_context_data(**kwargs)

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

        # print('data:', data)

        # TODO: Error handling
        try:
            ann = Announcement.objects.create(**data)
            ann.save()
        except Exception as e:
            print('ERROR:', str(e))
            return redirect('/')

        # return render(request, "user/create.html", context)
        return redirect('/user/create')


class AddEditAnnouncementHandler(TemplateView):
    template_name = 'user/create.html'

class MapView(TemplateView):
    template_name = 'user/map.html'

class PetView(TemplateView):
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
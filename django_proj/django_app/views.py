from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Manager
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from .models import User, Announcement

import MySQLdb
import os

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

    def post(self, request, **kwargs):
        form_type = request.POST.get('form_type')

        # Login form handler
        if form_type == 'username':
            login_email_or_name = request.POST.get('login_email')
            login_password = request.POST.get('login_password')

            try:
                # This branch will be executed if user entered email
                user = User.objects.get(email=login_email_or_name)
                if user.password != login_password:
                    # If there is no user with defined email and password
                    # say to user 'authentication failed'

                    context = super(HomePageView, self).get_context_data(**kwargs)
                    context['user_not_exists'] = True

                    # return redirect('/user/account/wrpass')
                    return render(request, "index.html", context)
                else:
                    # Authentication succeed so redirect to user's account page

                    context = super(HomePageView, self).get_context_data(**kwargs)
                    context['user_not_exists'] = False

                    return redirect('/user/account/' + user.username)
            except:
                try:
                    # This branch will be executed if user entered username
                    user = User.objects.get(username=login_email_or_name)
                    if user.password != login_password:
                        # If there is no user with defined email and password
                        # say to user 'authentication failed'

                        context = super(HomePageView, self).get_context_data(**kwargs)
                        context['user_not_exists'] = True

                        # return redirect('/user/account/wrpass')
                        return render(request, "index.html", context)
                    else:
                        # Authentication succeed so redirect to user's account page

                        context = super(HomePageView, self).get_context_data(**kwargs)
                        context['user_not_exists'] = False

                        return redirect('/user/account/' + user.username)
                except:
                    # This branch will be executed if user with specified username/email isn't existed
                    # If there is no user with defined email
                    # say to user 'authentication failed'
                    context = super(HomePageView, self).get_context_data(**kwargs)
                    context['user_not_exists'] = True

                    return render(request, "index.html", context)
        # Registration form handler
        elif form_type == 'registration':
            register_email = request.POST.get('register_email')
            register_name = request.POST.get('register_name')
            register_pass = request.POST.get('register_pass')
            register_pass2 = request.POST.get('register_pass2')

            try:
                user = User.objects.create(
                    email=register_email,
                    username=register_name,
                    password=register_pass
                )

                if register_pass != register_pass2:
                    # user registration was unsuccessful
                    # so we need to say this to him

                    context = super(HomePageView, self).get_context_data(**kwargs)
                    context['pass_not_match'] = True

                    return render(request, "index.html", context)
                else:
                    user.save()

                # send_mail(
                #     'Registration',
                #     'You are successfully registered!',
                #     'from@example.com',
                #     ['svs9119@yandex.ru'],
                #     fail_silently=False,
                # )

                # if user registration successful then say this to him
                # and redirect him to his new account

                # TODO: Maybe we shouldn't let user enter to his account until he confirms email?
                return redirect('/user/account/' + register_name)
            except:
                # user registration was unsuccessful
                # so we need to say this to him

                context = super(HomePageView, self).get_context_data(**kwargs)

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

class AccountView(TemplateView):
    template_name = 'user/account.html'


class AddAnnouncementView(TemplateView):
    template_name = 'user/create.html'

    def post(self, request: WSGIRequest, **kwargs):
        context = self.get_context_data(**kwargs)

        # TODO: Auth
        mgr: Manager = User.objects
        user_obj = mgr.all()[0]

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
            'user_obj': user_obj
        }

        # print('data:', data)

        # TODO: Error handling
        try:
            ann = Announcement.objects.create(**data)
            ann.save()
        except Exception as e:
            print('ERROR:', str(e))

        return render(request, "user/create.html", context)


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
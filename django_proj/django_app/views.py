from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect

from .models import User

import MySQLdb
import os

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'index.html'

class AccountView(TemplateView):
    template_name = 'user/account.html'

class AddAnnouncementView(TemplateView):
    template_name = 'user/create.html'

class AddEditAnnouncementHandler(TemplateView):
    template_name = 'user/create.html'

class MapView(TemplateView):
    template_name = 'user/map.html'

class PetView(TemplateView):
    template_name = 'user/pet.html'

class RegistrationView(TemplateView):
    template_name = 'user/registration.html'

class RegistrationHandler(TemplateView):
    template_name = 'user/registration.html'

    def post(self, request, **kwargs):
        # Company Info
        register_email = request.POST.get('register_email')
        register_pass = request.POST.get('register_pass')

        try:
            user = User.objects.create(
                email=register_email,
                password=register_pass
            )
            user.save()

            # if user registration successful then say this to him
            # and redirect him to his new account

            # context = super(RegistrationHandler, self).get_context_data(**kwargs)
            # context['registration_failed'] = False

            return redirect('/user/account/' + register_email)
        except:
            # user registration was unsuccessful
            # so we need to say this to him
            # redirection to main page is stub for now

            # context = super(RegistrationHandler, self).get_context_data(**kwargs)
            # context['registration_failed'] = True

            return redirect('/')


class LoginHandler(TemplateView):
    template_name = 'user/login.html'

    def post(self, request, **kwargs):
        # Company Info
        login_email =       request.POST.get('login_email')
        login_password =    request.POST.get('login_password')

        try:
            user = User.objects.get(email=login_email)
            if user.password != login_password:
                # If there is no user with defined email and password
                # say to user 'authentication failed'

                # context = super(LoginHandler, self).get_context_data(**kwargs)
                # context['user_not_exists'] = True

                return redirect('/')
            else:
                # Authentication succeed so redirect to user's account page

                # context = super(LoginHandler, self).get_context_data(**kwargs)
                # context['user_not_exists'] = False

                return redirect('/user/account/' + user.email)
        except:
            # If there is no user with defined email
            # say to user 'authentication failed'

            # context = super(LoginHandler, self).get_context_data(**kwargs)
            # context['user_not_exists'] = True

            return redirect('/')


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

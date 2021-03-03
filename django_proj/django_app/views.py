from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpResponse
from django.conf import settings

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

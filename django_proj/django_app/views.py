from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.conf import settings

import MySQLdb


def index(request):
    info = 'MySQL Server Version: '

    db = MySQLdb.connect(
        host=settings.DATABASES['default']['HOST'], 
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

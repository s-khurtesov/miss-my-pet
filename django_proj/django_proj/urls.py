from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('django_app/', include('django_app.urls')),
    path('admin/', admin.site.urls),
]

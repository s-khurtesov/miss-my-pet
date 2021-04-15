from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django_app import views, admin_views

urlpatterns = [
    # url allows define which page must be connected with the url
    # first field is regular expression that identifies url address
    # next field allows connect one of the classes in views.py file with some page
    # last filed i don't know exactly which meaning has but it usually has value of last url word

    # Home page is index.html
    url(r'^$', views.HomePageView.as_view(), name='index'),

    # User Views
    url(r'^user/account/([\w\-]+)', views.AccountView.as_view(), name='account'),
    url(r'^user/pet', views.PetView.as_view(), name='pet'),
    url(r'^user/map', views.MapView.as_view(), name='map'),
    url(r'^user/create', views.AddAnnouncementView.as_view(), name='create'),

    # Admin Views
    url(r'^admin/account/?$', admin_views.AccountView.as_view(), name='admin_account'),
    url(r'^admin/account/users/?$', admin_views.ObjectsListView.as_view(), name='admin_users'),
    url(r'^admin/account/announcements/?$', admin_views.ObjectsListView.as_view(), name='admin_announcements'),

    # this regex means that any URL "user/edit/<any word or/and any number>" is allowed
    # url(r'^user/edit/([\w\-]+)', views.AddEditAnnouncementHandler.as_view(), name='edit'),
]

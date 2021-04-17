from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django_app import views, admin_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # url allows define which page must be connected with the url
    # first field is regular expression that identifies url address
    # next field allows connect one of the classes in views.py file with some page
    # last filed i don't know exactly which meaning has but it usually has value of last url word

    # Home page is index.html
    url(r'^$', views.HomePageView.as_view(), name='index'),

    # User Views
    url(r'^user/account/?$', views.AccountView.as_view(), name='account'),
    url(r'^user/pet/?$', views.PetView.as_view(), name='pet'),
    url(r'^user/map/?$', views.MapView.as_view(), name='map'),
    url(r'^user/create/?$', views.AddAnnouncementView.as_view(), name='create'),
    url(r'^user/announcements/?$', views.AnnouncementsView.as_view(), name='user_announcements'),

    # Admin Views
    url(r'^admin/account/?$', admin_views.AccountView.as_view(), name='admin_account'),
    url(r'^admin/account/users/?$', admin_views.ObjectsListView.as_view(), name='admin_users'),
    url(r'^admin/account/announcements/?$', admin_views.ObjectsListView.as_view(), name='admin_announcements'),

    path('activate/<uidb64>/<token>/',views.activate, name='activate'),

    # Forget Password
    path('password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='index.html',
            extra_context={'password_reset': True}
        ),
        name='password_reset'),
    path('password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='index.html', 
            extra_context={'password_reset_done': True}
        ),
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='index.html', 
            extra_context={'password_reset_confirm': True}
        ),
        name='password_reset_confirm'),
    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='index.html', 
            extra_context={'password_reset_complete': True}
        ),
        name='password_reset_complete'),
]

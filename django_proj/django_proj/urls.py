from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django_app import views

urlpatterns = [
    # url allows define which page must be connected with the url
    # first field is regular expression that identifies url address
    # next field allows connect one of the classes in views.py file with some page
    # last filed i don't know exactly which meaning has but it usually has value of last url word
    # commented examples of url() functions (or classes - i don't sure) are from test django project and works fine
    # uncommented urls we use at our project

    # Home page is index.html
    url(r'^$', views.HomePageView.as_view(), name='index'),

    # User Views
    url(r'^user/registration', views.RegistrationView.as_view(), name='registration'),
    url(r'^user/account', views.AccountView.as_view(), name='account'),
    url(r'^user/pet', views.PetView.as_view(), name='pet'),
    url(r'^user/map', views.MapView.as_view(), name='map'),
    url(r'^user/create', views.AddAnnouncementView.as_view(), name='create'),

    # this regex means that any URL "user/edit/<any word or/and any number>" is allowed
    url(r'^user/edit/([\w\-]+)', views.AddEditAnnouncementHandler.as_view(), name='edit'),


    # url(r'^details/([\w\-]+)/?$', views.JobDetails.as_view(), name='details'),
    #
    # # Admin Views
    # url(r'^admin/settings', admin_views.SettingsView.as_view(), name='settings'),
    # url(r'^admin/create', admin_views.AddJobView.as_view(), name='create'),
    # url(r'^admin/edit/([\w\-]+)',   admin_views.AddEditJobHandler.as_view(), name='edit'),
    #
    # #Admin Handlers
    # url(r'^admin/post', admin_views.AddEditJobHandler.as_view(), name='post'),
    # url(r'^admin/delete', admin_views.DeleteJobHandler.as_view(),  name='delete'),
    #
    # url(r'^admin/', admin_views.DashboardView.as_view(), name='admin'),


    # path('django_app/', include('django_app.urls')),
    # path('admin/', admin.site.urls),
]

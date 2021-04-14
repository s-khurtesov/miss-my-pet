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


class LoginView(TemplateView):
    template_name = 'admin/login.html'

    def post(self, request: WSGIRequest, **kwargs):
        login = request.POST.get('login')
        password = request.POST.get('password')

        # TODO: How should we store admin credentials?
        if login == "admin" and password == "admin":
            return redirect('/admin/account/')
        else:
            context = super(LoginView, self).get_context_data(**kwargs)
            context['user_not_exists'] = True

            return render(request, "admin/login.html", context)


class AccountView(TemplateView):
    template_name = 'admin/account.html'

    def post(self, request: WSGIRequest, **kwargs):
        pass


class ObjectsListView(TemplateView):
    template_name = 'admin/objects_list.html'

    def post(self, request: WSGIRequest, **kwargs):
        context = super(ObjectsListView, self).get_context_data(**kwargs)

        form_type = request.POST.get('form_type')
        action = request.POST.get('action')

        if form_type == 'users':
            if action == 'delete':
                login = request.POST.get('user_login')
                u = User.objects.get(login=login)

                try:
                    # Deletes user from database.
                    u.delete()
                except:
                    return redirect('/')
            elif action == 'block':
                login = request.POST.get('user_login')
                u = User.objects.get(login=login)
                u.is_blocked = True
                u.save()

            elif action == 'unblock':
                login = request.POST.get('user_login')
                u = User.objects.get(login=login)
                u.is_blocked = False
                u.save()

            elif action == 'reset':
                login = request.POST.get('user_login')
                u = User.objects.get(login=login)
                u.password = None
                u.save()
            elif action != 'none':
                return redirect('/')

            context['users_list'] = True
            context['users'] = User.objects.all()
            return render(request, "admin/objects_list.html", context)
        elif form_type == 'announcements':
            if action == 'delete':
                ann_id = request.POST.get('ann_id')
                ann = Announcement.objects.get(id=ann_id)

                try:
                    # Deletes announcement from database.
                    ann.delete()
                except:
                    return redirect('/')
            elif action != 'none':
                return redirect('/')

            context['announcements'] = Announcement.objects.all()
            context['users_list'] = False
            return render(request, "admin/objects_list.html", context)
        else:
            return redirect('/')

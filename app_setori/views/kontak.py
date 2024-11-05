from django.shortcuts import render, redirect

from django.views import View

from django.shortcuts import render, redirect
from django.db import transaction 
from django.views import View
from admin_setori.models import Kontak
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django import forms
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from admin_setori.decorators import role_required

class KontakViews(View):
    def get(self, request):
        dt_kontak = Kontak.objects.filter(deleted_at__isnull = True)
        data = {
            'dt_kontak' : dt_kontak
        }
        return render(request, 'setori/kontak/index.html', data)
from django.shortcuts import render, redirect
from django.db import transaction 
from django.views import View
from admin_setori.models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django import forms
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from admin_setori.decorators import role_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

class PotensiViews(View):
    def get(self, request):
        dt_potensi = Info_wilayah.objects.filter(deleted_at__isnull = True)
        paginator = Paginator(dt_potensi, 4)  # Batasi 10 berita per halaman

        dt_penduduk = Data_penduduk.objects.filter(deleted_at__isnull = True)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        data = {
            'dt_potensi' : dt_potensi,
            'page_obj': page_obj,
            'dt_penduduk': dt_penduduk
        }
        return render(request, 'setori/potensidaerah/index.html', data)

class DistrikpotensiViews(View):
    def get(self, request):
        return render(request, 'setori/potensidaerah/distrik_lengkap.html')

class DetailpotensidistrikViews(View):
    def get(self, request):
        return render(request, 'setori/potensidaerah/detaildistrik.html')

class DetailpotensikampungViews(View):
    def get(self, request):
        return render(request, 'setori/potensidaerah/detail.html')
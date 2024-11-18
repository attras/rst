from django.shortcuts import render, redirect

from django.views import View

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

class HomeViews(View):
    def get(self, request):
        dt_slider = Slider.objects.filter(deleted_at__isnull = True)

        dt_berita = News.objects.filter(deleted_at__isnull=True).order_by('-created_at')  # Ambil semua berita yang tidak dihapus
        dt_kategori = Category.objects.filter(deleted_at__isnull=True)  # Ambil semua kategori yang tidak dihapus

        paginator = Paginator(dt_berita, 3)  # Batasi 10 berita per halaman

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        dt_tentang = Tentang.objects.filter(deleted_at__isnull = True).order_by('created_at')
        data = {
            'dt_slider' : dt_slider,
            'dt_berita': dt_berita,  # Ganti dengan data yang sudah dipaginate
            'dt_kategori': dt_kategori, 
            'page_obj': page_obj,
            'dt_tentang' : dt_tentang,
        }
        return render(request, 'setori/home/index.html', data)
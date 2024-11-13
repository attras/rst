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

class BeritaViews(View):
    def get(self, request):
        dt_berita = News.objects.filter(deleted_at__isnull=True).order_by('-created_at')  # Ambil semua berita yang tidak dihapus
        dt_kategori = Category.objects.filter(deleted_at__isnull=True)  # Ambil semua kategori yang tidak dihapus

        paginator = Paginator(dt_berita, 6)  # Batasi 10 berita per halaman

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        data = {
            'dt_berita': dt_berita,  # Ganti dengan data yang sudah dipaginate
            'dt_kategori': dt_kategori, 
            'page_obj': page_obj
        }
        return render(request, 'setori/berita/index.html', data)

class DetailberitaViews(View):
    def get(self, request, slug):
        detail_berita = get_object_or_404(News,slug=slug)
        dt_berita = News.objects.filter(deleted_at__isnull=True).order_by('-created_at')  # Ambil semua berita yang tidak dihapus
        dt_kategori = Category.objects.filter(deleted_at__isnull=True)  # Ambil semua kategori yang tidak dihapus

        paginator = Paginator(dt_berita, 6)  # Batasi jumlah berita yang ditampilkan per halaman (6 berita)
        page_number = request.GET.get('page')  # Ambil nomor halaman dari query parameter
        page_obj = paginator.get_page(page_number)  # Ambil berita untuk halaman yang diminta

        data = {
            'dt_berita': dt_berita,
            'detail_berita': detail_berita,
            'dt_kategori': dt_kategori,
            'page_obj': page_obj
        }
        return render(request, 'setori/berita/detail_berita.html', data)
     
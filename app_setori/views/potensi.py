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
from django.db.models import Sum

class PotensiViews(View):
    def get(self, request):
        dt_potensi = Info_wilayah.objects.filter(wilayah__wilayah_level="4", deleted_at__isnull=True)
        paginator = Paginator(dt_potensi, 1)  # Batasi 10 berita per halaman

        dt_penduduk = Data_penduduk.objects.filter(deleted_at__isnull = True)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        total = (
            Data_penduduk.objects
            .values('wilayah__wilayah_parent__wilayah_nama')
            .annotate(total_pria_oap=Sum('pria_oap'),
                      total_pria_non_oap=Sum('pria_non_oap'),
                      total_wanita_oap=Sum('wanita_oap'),
                      total_wanita_non_oap=Sum('wanita_non_oap'),
                      total_jumlah_kk_oap=Sum('jumlah_kk_oap'),
                      total_jumlah_kk_non_oap=Sum('jumlah_kk_non_oap'),
                      )
            .order_by('wilayah__wilayah_parent__wilayah_nama')
        )

        data = {
            'dt_potensi' : dt_potensi,
            'page_obj': page_obj,
            'dt_penduduk': dt_penduduk,
            'total' : total

        }
        return render(request, 'setori/potensidaerah/index.html', data)


class PotensiDistrikViews(View):
    def get(self, request):
        dt_potensi = Info_wilayah.objects.filter(wilayah__wilayah_level="3", deleted_at__isnull=True)
        paginator = Paginator(dt_potensi, 1)  # Batasi 10 berita per halaman

        dt_penduduk = Data_penduduk.objects.filter(deleted_at__isnull = True)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        data = {
            'dt_potensi' : dt_potensi,
            'page_obj': page_obj,
            'dt_penduduk': dt_penduduk
        }
        return render(request, 'setori/potensidaerah/index.html', data)

class DistridetailViews(View):
    def get(self, request, info_wilayah_id):
        dt_info_wilayah = get_object_or_404(Info_wilayah, info_wilayah_id=info_wilayah_id, deleted_at__isnull=True)

        dt_wilayah_penduduk = Data_penduduk.objects.filter(wilayah=dt_info_wilayah.wilayah, deleted_at__isnull=True)
        dt_sarpras = Data_sarpras.objects.filter(wilayah=dt_info_wilayah.wilayah, deleted_at__isnull=True)
        data = (
            Data_penduduk.objects
            .filter(wilayah__wilayah_parent= dt_info_wilayah.wilayah)
            .values('wilayah__wilayah_parent__wilayah_nama')
            .annotate(total_jiwa=Sum('total_penduduk'),
                      total_pria_oap=Sum('pria_non_oap'),
                      total_pria_non_oap=Sum('pria_non_oap'),
                      total_wanita_oap=Sum('wanita_oap'),
                      total_wanita_non_oap=Sum('wanita_non_oap'),
                      total_oap=Sum('jumlah_penduduk_oap'),
                      total_non_oap=Sum('jumlah_penduduk_non_oap'),
                      )
         
        )
        data = {
            'dt_info_wilayah' : dt_info_wilayah,
            'dt_wilayah_penduduk' : dt_wilayah_penduduk,
            'data' : data,
            'dt_sarpras' : dt_sarpras,
        }
        return render(request, 'setori/potensidaerah/detail.html', data)


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
from django.db.models import Sum
from admin_setori.decorators import role_required
from django.utils.decorators import method_decorator

class Data_pokokViews(View):
    def get(self, request):
        wilayah_list = MasterWilayah.objects.filter(deleted_at__isnull=True)
        dt_penduduk = Data_penduduk.objects.filter(deleted_at__isnull=True)
        total_kk_semua = Data_penduduk.objects.aggregate(total=Sum('total_kk'))['total']

        # wanita total
        total_wanita_oap = Data_penduduk.objects.aggregate(total_oap=Sum('wanita_oap'))['total_oap']
        total_wanita_non_oap = Data_penduduk.objects.aggregate(total_non_oap=Sum('wanita_non_oap'))['total_non_oap']

        total_wanita_semua = total_wanita_oap + total_wanita_non_oap or 0

        # pria total
        total_pria_oap = Data_penduduk.objects.aggregate(total_oap=Sum('pria_oap'))['total_oap']
        total_pria_non_oap = Data_penduduk.objects.aggregate(total_non_oap=Sum('pria_non_oap'))['total_non_oap']

        total_pria_semua = total_pria_oap + total_pria_non_oap or 0

        # penduduk total
        total_penduduk_semua = total_pria_semua + total_wanita_semua or 0

        # total oap
        total_oap = total_pria_oap + total_wanita_oap or 0

        # total non oap
        total_non_oap = total_wanita_non_oap + total_pria_non_oap or 0

        # kesehatan
        dt_kesehatan = Data_kesehatan.objects.filter(deleted_at__isnull=True)
        jenis_kesehatan = Master_jenis_kesehatan.objects.filter(deleted_at__isnull=True)
        dt_indikator = Indikator_kesehatan.objects.filter(deleted_at__isnull=True)
        wilayah_list = MasterWilayah.objects.filter(deleted_at__isnull=True)

        # Membuat array indikator
        dt_array_indikator = list(dt_indikator.values('id_indikator', 'nama_indikator',)) 
        dt_array_jenis = list(jenis_kesehatan.values('nama_jenis',))
        dt_array_kesehatan = list(dt_kesehatan.values('oap', 'non_oap')) # Sesuaikan dengan field yang ada

        data = {
            'dt_penduduk': dt_penduduk,
            'total_kk_semua': total_kk_semua,
            'total_wanita_semua': total_wanita_semua,
            'total_pria_semua': total_pria_semua,
            'total_penduduk_semua': total_penduduk_semua,
            'total_oap': total_oap,
            'total_non_oap': total_non_oap,
            'wilayah_list': wilayah_list,
            'jenis_kesehatan': jenis_kesehatan,
            'wilayah_list': wilayah_list,
            'dt_kesehatan': dt_kesehatan,
            'dt_array_indikator': dt_array_indikator,
            'dt_array_jenis': dt_array_jenis,
            'dt_array_kesehatan': dt_array_kesehatan,
        }
        return render(request, 'setori/data_pokok/index.html', data)

class DetaildataViews(View):
    def get(self, request):
        return render(request, 'setori/data_pokok/data_rinci.html')
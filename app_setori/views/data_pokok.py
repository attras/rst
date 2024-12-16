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
        
        jumlah = Data_penduduk.objects.aggregate(
        total_pria=Sum('pria_oap') + Sum('pria_non_oap'),
        total_wanita=Sum('wanita_oap') + Sum('wanita_non_oap'),
        total_oap = Sum('pria_oap') + Sum('wanita_oap'),
        total_non_oap = Sum('pria_non_oap') + Sum('wanita_non_oap'),
        total_kk=Sum('total_kk'),
        total_penduduk=Sum('total_penduduk'),
    )
        # kesehatan
        dt_kesehatan = Data_kesehatan.objects.filter(deleted_at__isnull=True)
        jenis_kesehatan = Master_jenis_kesehatan.objects.filter(deleted_at__isnull=True)
        dt_indikator = Indikator_kesehatan.objects.filter(deleted_at__isnull=True)
        wilayah_list = MasterWilayah.objects.filter(deleted_at__isnull=True)

        # Membuat array indikator
        dt_array_indikator = list(dt_indikator.values('id_indikator', 'nama_indikator',)) 
        dt_array_jenis = list(jenis_kesehatan.values('nama_jenis',))
        dt_array_kesehatan = list(dt_kesehatan.values('oap', 'non_oap')) # Sesuaikan dengan field yang ada

      
        # Ambil semua data dari model Data_kesehatan
        data = Data_kesehatan.objects.select_related('wilayah', 'fk_jenis', 'indikator').all()

        # Siapkan array untuk menangkap data
        all_data = []

        # Loop data untuk memasukkan setiap atribut ke dalam array
        for entry in data:
            all_data.append({
                "data_kesehatan_id": str(entry.data_kesehatan_id),
                "wilayah": entry.wilayah.wilayah_nama if entry.wilayah else "N/A",
                "fk_jenis": entry.fk_jenis.nama_jenis if entry.fk_jenis else "N/A",
                "indikator": entry.indikator.nama_indikator if entry.indikator else "N/A",
                "oap": entry.oap,
                "non_oap": entry.non_oap
            })

        print(all_data)

       

        
        data = {
            'dt_penduduk': dt_penduduk,
            'jumlah':jumlah,
            'wilayah_list': wilayah_list,
            'jenis_kesehatan': jenis_kesehatan,
            'wilayah_list': wilayah_list,
            'dt_kesehatan': dt_kesehatan,
            'dt_array_indikator': dt_array_indikator,
            'dt_array_jenis': dt_array_jenis,
            'dt_array_kesehatan': dt_array_kesehatan,
            'all_data': all_data
           
        }
        return render(request, 'setori/data_pokok/index.html', data)
    
class KesehatanDataViews(View):
    # Mengirimkan data JSON
    def get(self, request):
        wilayah_filter = request.GET.get('wilayah', None)  # Dapatkan filter wilayah dari query string
        data_queryset = Data_kesehatan.objects.filter(wilayah__wilayah_level=4,deleted_at__isnull=True)  # Hanya level 4
        
        # Terapkan filter wilayah jika ada
        if wilayah_filter:
            data_queryset = data_queryset.filter(wilayah__wilayah_nama=wilayah_filter)

        grouped_data = {}
        for item in data_queryset:
            jenis = item.fk_jenis.nama_jenis
            if jenis not in grouped_data:
                grouped_data[jenis] = {
                    "categories": [],
                    "oap": [],
                    "non_oap": []
                }
      
            grouped_data[jenis]["categories"].append(item.indikator.nama_indikator)
            grouped_data[jenis]["oap"].append(item.oap)
            grouped_data[jenis]["non_oap"].append(item.non_oap)
        print(grouped_data)
        # Semua wilayah untuk dropdown
        wilayah_list = Data_kesehatan.objects.values_list(
            'wilayah__wilayah_nama', flat=True
        ).distinct()

        return JsonResponse({
            "data": grouped_data,
            "wilayah_list": list(wilayah_list)
        })

class DetaildataViews(View):
    def get(self, request):
        return render(request, 'setori/data_pokok/data_rinci.html')
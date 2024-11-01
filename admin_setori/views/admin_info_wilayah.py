from django.shortcuts import render, redirect
from django.db import transaction 
from django.views import View
from admin_setori.models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from admin_setori.decorators import role_required
from django.utils.decorators import method_decorator

@method_decorator(login_required(), name='dispatch')
class Info_wilayahViews(View):
    def get(self, request):
        dt_info_wilayah = Info_wilayah.objects.filter(deleted_at__isnull = True)
        pilih_wilayah = MasterWilayah.objects.filter(deleted_at__isnull = True)
        data = {
            'dt_info_wilayah' : dt_info_wilayah,
            'pilih_wilayah' : pilih_wilayah
        }

        return render(request, 'admin/admin_info_wilayah/index.html',data)
    
class AddInfoWilayah(View):
  
    def post(self, request):
        visi = request.POST.get('visi')
        misi = request.POST.get('misi')
        nama_info_wilayah = request.POST.get('nama_info_wilayah')
        kode_info_wilayah = request.POST.get('kode_info_wilayah')
        tahun_pembentukan = request.POST.get('tahun_pembentukan')
        dasar_hukum_pembentukan = request.POST.get('dasar_hukum_pembentukan')
        kode_pos = request.POST.get('kode_pos')
        wilayah_id = request.POST.get('wilayah')

        try:
            with transaction.atomic():
                info_wilayah = Info_wilayah(
                    visi=visi,
                    misi=misi,
                    nama_info_wilayah=nama_info_wilayah,
                    kode_info_wilayah=kode_info_wilayah,
                    tahun_pembentukan=tahun_pembentukan,
                    dasar_hukum_pembentukan=dasar_hukum_pembentukan,
                    kode_pos=kode_pos,
                    wilayah=MasterWilayah.objects.get(wilayah_id=wilayah_id)
                )
                info_wilayah.save()

                messages.success(request, "Data Info Wilayah berhasil ditambahkan.")
                return redirect('admin_setori:admin_info_wilayah')  # Ubah dengan nama URL yang sesuai

        except Exception as e:
            print("Error Data:", e)
            messages.error(request, "Gagal menambahkan data Info Wilayah.")
            return redirect('admin_setori:admin_info_wilayah')  # Ubah dengan nama URL yang sesuai
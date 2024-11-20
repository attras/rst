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
from django.core.exceptions import ObjectDoesNotExist


@method_decorator(login_required(), name='dispatch')
class Info_wilayahViews(View):
    def get(self, request):
        dt_wilayah = MasterWilayah.objects.filter(deleted_at__isnull=True).order_by('wilayah_level')

        data = {
            'dt_wilayah': dt_wilayah,
            'LEVEL_WILAYAH': LEVEL_WILAYAH,
            
        }

        return render(request, 'admin/admin_info_wilayah/index.html',data)

class Detail_info_wilayah(View):
    def get(self, request,wilayah_id):
        dt_info_wilayah = Info_wilayah.objects.filter(deleted_at__isnull = True,wilayah_id=wilayah_id)
        pilih_wilayah = MasterWilayah.objects.filter(deleted_at__isnull = True,wilayah_id=wilayah_id)
        try:
            data_info_wilayah =  Info_wilayah.objects.get(wilayah_id=wilayah_id, deleted_at__isnull=True)
        # Jika ada data penduduk, ambil semua field
        except ObjectDoesNotExist:
            data_info_wilayah = None  # Atau menangani error sesuai kebutuhan


        data = {
            'dt_info_wilayah' : dt_info_wilayah,
            'pilih_wilayah' : pilih_wilayah,
            'wilayah_id' : wilayah_id,
            'data_info_wilayah' : data_info_wilayah,
        }
        
        return render(request, 'admin/admin_info_wilayah/detail.html',data)


class AddInfoWilayah(View):
    def get(self, request,wilayah_id):
        dt_info_wilayah = Info_wilayah.objects.filter(deleted_at__isnull = True,wilayah_id=wilayah_id)
        pilih_wilayah = MasterWilayah.objects.filter(deleted_at__isnull = True,wilayah_id=wilayah_id).first()
        data = {
            'dt_info_wilayah' : dt_info_wilayah,
            'pilih_wilayah' : pilih_wilayah,
            'wilayah_id' : wilayah_id,
       
        }
        
        return render(request, 'admin/admin_info_wilayah/form.html',data)

class InfoWilayahAdd(View):
    def post(self, request):
        visi = request.POST.get('visi')
        misi = request.POST.get('misi')
        kode_info_wilayah = request.POST.get('kode_info_wilayah')
        tahun_pembentukan = request.POST.get('tahun_pembentukan')
        kode_pos = request.POST.get('kode_pos')
        link_maps = request.POST.get('map')
        image_profile = request.FILES.get('profil')
        wilayah_id = request.POST.get('wilayah')
       
        try:
            with transaction.atomic():
                

                info_wilayah = Info_wilayah()
                info_wilayah.visi = visi
                info_wilayah.misi = misi
                info_wilayah.kode_info_wilayah=kode_info_wilayah
                info_wilayah.tahun_pembentukan=tahun_pembentukan
                info_wilayah.kode_pos=kode_pos
                info_wilayah.wilayah_id = wilayah_id
                info_wilayah.link_maps=link_maps
                info_wilayah.image_profile= image_profile

                info_wilayah.save()


                messages.success(request, "Data Info Wilayah berhasil ditambahkan.")
                return redirect('admin_setori:detail_info_wilayah', wilayah_id)  # Ubah dengan nama URL yang sesuai

        except Exception as e:
            print("Error Data:", e)
            messages.error(request, "Gagal menambahkan data Info Wilayah.")
            return redirect('admin_setori:admin_info_wilayah',wilayah_id)  # Ubah dengan nama URL yang sesuai
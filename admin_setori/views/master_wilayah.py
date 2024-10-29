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

@method_decorator(login_required(), name='dispatch')
class Master_wilayahViews(View):
    def get(self, request):
        dt_wilayah = MasterWilayah.objects.filter(deleted_at__isnull=True)
        provinsi_choices = MasterWilayah.objects.filter(wilayah_level='1')
        kabupaten_choices = MasterWilayah.objects.filter(wilayah_level='2')
        kecamatan_choices = MasterWilayah.objects.filter(wilayah_level='3')
        
        data = {
            'dt_wilayah': dt_wilayah,
            'provinsi_choices': provinsi_choices,
            'kabupaten_choices': kabupaten_choices,
            'kecamatan_choices': kecamatan_choices,
            'LEVEL_WILAYAH': LEVEL_WILAYAH,
            
        }
        return render(request, 'admin/master_wilayah/index.html',data)
    
class AddWilayah(View):
 

    def post(self, request):
        wilayah_nama = request.POST.get('wilayah_nama')
        wilayah_level = request.POST.get('wilayah_level')
        wilayah_status = request.POST.get('wilayah_status') == 'on'

        # Tentukan wilayah_parent sesuai dengan aturan level
        wilayah_parent = None
        if wilayah_level == '2':  # Kabupaten
            wilayah_parent_id = request.POST.get('wilayah_parent_provinsi')
            wilayah_parent = MasterWilayah.objects.get(wilayah_id=wilayah_parent_id)
        elif wilayah_level == '3':  # Kecamatan
            wilayah_parent_id = request.POST.get('wilayah_parent_kabupaten')
            wilayah_parent = MasterWilayah.objects.get(wilayah_id=wilayah_parent_id)
        elif wilayah_level == '4':  # Kampung
            wilayah_parent_id = request.POST.get('wilayah_parent_kecamatan')
            wilayah_parent = MasterWilayah.objects.get(wilayah_id=wilayah_parent_id)

        try:
            with transaction.atomic():
                master_wilayah = MasterWilayah(
                    wilayah_nama=wilayah_nama,
                    wilayah_level=wilayah_level,
                    wilayah_status=wilayah_status,
                    wilayah_parent=wilayah_parent
                )
                master_wilayah.save()

                messages.success(request, "Data Wilayah berhasil ditambahkan.")
                return redirect('admin_setori:master_wilayah')  # Ubah dengan nama URL yang sesuai

        except Exception as e:
            print("Error Data:", e)
            messages.error(request, "Gagal menambahkan data Wilayah.")
            return redirect('admin_setori:master_wilayah')  # Ubah dengan nama URL yang sesuai
        
class DeleteWilayah(View):
    def get(self, request, wilayah_id):
        del_wilayah = get_object_or_404(MasterWilayah, wilayah_id=wilayah_id)
        
        try:
            with transaction.atomic():
                del_wilayah.delete()
                messages.success(request, "Data berhasil dihapus")
        except Exception as e:
            print('Error Data:', e)
            messages.error(request, "Gagal menghapus data")
        
        return redirect('admin_setori:master_wilayah')
    

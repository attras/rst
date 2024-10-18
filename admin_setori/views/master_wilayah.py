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
        data = {
            'dt_wilayah': dt_wilayah,
            'level':LEVEL_WILAYAH
        }
        return render(request, 'admin/master_wilayah/index.html',data)
    
class AddWilayah(View):
     def post(self, request):
        wilayah_nama = request.POST.get('wilayah_nama')
        wilayah_level = request.POST.get('wilayah_level')
        wilayah_parent_id = request.POST.get('wilayah_parent')

        # Validasi manual
        wilayah_parent = MasterWilayah.objects.filter(wilayah_id=wilayah_parent_id).first()
        
        if wilayah_level == '3':  # Jika level adalah 'Kampung'
            if not wilayah_parent or wilayah_parent.wilayah_level != '2':
                messages.error(request, "Kampung harus dipilih dari Kecamatan yang sudah ada.")
                return redirect('admin_setori:master_wilayah')

        elif wilayah_level == '2':  # Jika level adalah 'Kecamatan'
            if not wilayah_parent or wilayah_parent.wilayah_level != '1':
                messages.error(request, "Kecamatan harus dipilih dari Kabupaten yang sudah ada.")
                return redirect('admin_setori:master_wilayah')

        # Jika validasi lolos, simpan data
        try:
            with transaction.atomic():
                insert_wilayah = MasterWilayah()
                insert_wilayah.wilayah_nama = wilayah_nama
                insert_wilayah.wilayah_level = wilayah_level
                insert_wilayah.wilayah_parent = wilayah_parent
                insert_wilayah.wilayah_id = uuid.uuid4()  # Generate new UUID
                insert_wilayah.save()

                messages.success(request, "Data berhasil ditambahkan")
                return redirect('admin_setori:master_wilayah')
        except Exception as e:
            print('Error Data:', e)
            messages.error(request, "Gagal menambahkan data")
            return redirect('admin_setori:master_wilayah')
        
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
    

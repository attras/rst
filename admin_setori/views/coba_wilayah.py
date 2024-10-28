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
class Coba_wilayahViews(View):
    def get(self, request):
        dt_wilayah = CobaWilayah.objects.filter(deleted_at__isnull=True)
        kabupaten_choices = CobaWilayah.objects.filter(wilayah_level='1')
        kecamatan_choices = CobaWilayah.objects.filter(wilayah_level='2')
        context = {
            'dt_wilayah': dt_wilayah,
            'LEVEL_WILAYAH': LEVEL_WILAYAH,
            'kabupaten_choices': kabupaten_choices,
            'kecamatan_choices': kecamatan_choices,
        }
       
        return render(request, 'admin/coba_wilayah/index.html',context)

class AddCobaWilayah(View):
     def post(self, request):
        wilayah_nama = request.POST.get('wilayah_nama')
        wilayah_level = request.POST.get('wilayah_level')
        asal_kabupaten = request.POST.get('asal_kabupaten', None)
        asal_kecamatan = request.POST.get('asal_kecamatan', None)
        nama_kampung = request.POST.get('nama_kampung', None)

        try:
            with transaction.atomic():
                insert_wilayah = CobaWilayah()
                insert_wilayah.wilayah_nama = wilayah_nama
                insert_wilayah.wilayah_level = wilayah_level

                if wilayah_level == '1':
                    # Level 1: Kabupaten
                    insert_wilayah.asal_kabupaten = wilayah_nama
                    insert_wilayah.asal_kecamatan = None
                    insert_wilayah.nama_kampung = None

                elif wilayah_level == '2':
                    # Level 2: Kecamatan, pilih dari kabupaten yang sudah ada
                    insert_wilayah.asal_kabupaten = asal_kabupaten
                    insert_wilayah.asal_kecamatan = wilayah_nama
                    insert_wilayah.nama_kampung = None

                elif wilayah_level == '3':
                    # Level 3: Kampung, pilih dari kabupaten dan kecamatan yang sudah ada
                    insert_wilayah.asal_kabupaten = asal_kabupaten
                    insert_wilayah.asal_kecamatan = asal_kecamatan
                    insert_wilayah.nama_kampung = wilayah_nama

                insert_wilayah.created_at = timezone.now()
                insert_wilayah.save()

                messages.success(request, "Data Wilayah berhasil ditambahkan")
                return redirect('admin_setori:coba_wilayah')

        except Exception as e:
            print('Error Data:', e)
            messages.error(request, "Gagal menambahkan data wilayah")
            return redirect('admin_setori:coba_wilayah')
        


class EditCobaWilayah(View):
    def get(self, request, wilayah_id):
        wilayah = get_object_or_404(CobaWilayah, wilayah_id=wilayah_id)
        
        kabupaten_choices = CobaWilayah.objects.filter(wilayah_level='1')
        kecamatan_choices = CobaWilayah.objects.filter(wilayah_level='2')

        context = {
            'wilayah': wilayah,
            'LEVEL_WILAYAH': CobaWilayah.LEVEL_WILAYAH,
            'kabupaten_choices': kabupaten_choices,
            'kecamatan_choices': kecamatan_choices,
        }
        return render(request, 'edit_wilayah.html', context)

    def post(self, request, wilayah_id):
        wilayah = get_object_or_404(CobaWilayah, wilayah_id=wilayah_id)
        wilayah_nama = request.POST.get('wilayah_nama')
        wilayah_level = request.POST.get('wilayah_level')
        asal_kabupaten = request.POST.get('asal_kabupaten', None)
        asal_kecamatan = request.POST.get('asal_kecamatan', None)
        nama_kampung = request.POST.get('nama_kampung', None)

        try:
            with transaction.atomic():
                wilayah.wilayah_nama = wilayah_nama
                wilayah.wilayah_level = wilayah_level

                if wilayah_level == '1':
                    wilayah.asal_kabupaten = wilayah_nama
                    wilayah.asal_kecamatan = None
                    wilayah.nama_kampung = None

                elif wilayah_level == '2':
                    wilayah.asal_kabupaten = asal_kabupaten
                    wilayah.asal_kecamatan = wilayah_nama
                    wilayah.nama_kampung = None

                elif wilayah_level == '3':
                    wilayah.asal_kabupaten = asal_kabupaten
                    wilayah.asal_kecamatan = asal_kecamatan
                    wilayah.nama_kampung = wilayah_nama

                wilayah.save()

                messages.success(request, "Data Wilayah berhasil diperbarui.")
                return redirect('list_wilayah')  # Ganti dengan URL untuk halaman daftar wilayah

        except Exception as e:
            print("Error Data:", e)
            messages.error(request, "Gagal memperbarui data wilayah.")
            return redirect('edit_wilayah', wilayah_id=wilayah_id)

        
class DeleteCobaWilayah(View):
    def post(self, request, wilayah_id):
        try:
            with transaction.atomic():
                wilayah = get_object_or_404(CobaWilayah, wilayah_id=wilayah_id)
                wilayah.delete()
                messages.success(request, "Data wilayah berhasil dihapus.")
                return redirect('admin_setori:coba_wilayah')  # Ubah sesuai dengan nama URL halaman daftar wilayah

        except Exception as e:
            print("Error Data:", e)
            messages.error(request, "Gagal menghapus data wilayah.")
            return redirect('admin_setori:coba_wilayah')
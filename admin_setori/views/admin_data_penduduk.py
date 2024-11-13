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

@method_decorator(login_required(), name='dispatch')
class Admin_data_pendudukViews(View):
    def get(self, request):
        wilayah_list = MasterWilayah.objects.filter(deleted_at__isnull = True)
        dt_penduduk = Data_penduduk.objects.filter(deleted_at__isnull = True)

        data={
            'dt_penduduk': dt_penduduk,
            'wilayah_list': wilayah_list
        }
        

        return render(request, 'admin/admin_data_penduduk/index.html',data)

class Add_data_penduduk(View):
    def post(self, request):

         
        
       
        wilayah_id = request.POST.get("wilayah")
         # Cek apakah wilayah sudah ada di model Data_penduduk
        if Data_penduduk.objects.filter(wilayah_id=wilayah_id).exists():
            messages.error(request, "Data untuk wilayah ini sudah ada.")
            return redirect("admin_setori:data_penduduk")
        
        pria_oap = int(request.POST.get("pria_oap", 0))
        pria_non_oap = int(request.POST.get("pria_non_oap", 0))
        wanita_oap = int(request.POST.get("wanita_oap", 0))
        wanita_non_oap = int(request.POST.get("wanita_non_oap", 0))
        jumlah_kk_oap = int(request.POST.get("jumlah_kk_oap", 0))
        jumlah_kk_non_oap = int(request.POST.get("jumlah_kk_non_oap", 0))

        try:
            with transaction.atomic():
                wilayah = MasterWilayah.objects.get(pk=wilayah_id)
                data_penduduk = Data_penduduk(
                    wilayah=wilayah,
                    pria_oap=pria_oap,
                    pria_non_oap=pria_non_oap,
                    wanita_oap=wanita_oap,
                    wanita_non_oap=wanita_non_oap,
                    jumlah_kk_oap=jumlah_kk_oap,
                    jumlah_kk_non_oap=jumlah_kk_non_oap
                )
                data_penduduk.save()

                

                messages.success(request, "Data penduduk berhasil ditambahkan.")
                return redirect("admin_setori:data_penduduk")  # Kembali ke form jika berhasil
            
        except Exception as e:
            print("Gagal menambahkan data:", e)
            messages.error(request, "Gagal menambahkan data penduduk.")
            return redirect("admin_setori:data_penduduk")  # Kembali ke form jika gagal
  
class DeletePenduduk(View):
    def get(self, request, data_penduduk_id):
        del_penduduk = get_object_or_404(Data_penduduk, data_penduduk_id=data_penduduk_id)
        
        try:
            with transaction.atomic():
                del_penduduk.delete()
                messages.success(request, "Data berhasil dihapus")
        except Exception as e:
            print('Error Data:', e)
            messages.error(request, "Gagal menghapus data")
        
        return redirect("admin_setori:data_penduduk")
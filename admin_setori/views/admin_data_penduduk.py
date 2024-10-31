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
class Admin_data_pendudukViews(View):
    def get(self, request):
        
        dt_data_penduduk = Data_peduduk.objects.select_related('wilayah').all()
        pilih_wilayah = MasterWilayah.objects.filter(deleted_at__isnull=True, wilayah_level=4)
        data = {
            'dt_data_penduduk' : dt_data_penduduk,
            'pilih_wilayah' : pilih_wilayah,
            'identitas_choices': IDENTITAS_CHOICE
        }
      
        return render(request, 'admin/admin_data_penduduk/index.html',data)

class Add_data_penduduk(View):
    def post(self, request):
        identitas = request.POST.get('identitas')
        pria = int(request.POST.get('pria', 0))
        wanita = int(request.POST.get('wanita', 0))
        jumlah_kk = int(request.POST.get('kk', 0))
        wilayah_id = request.POST.get('wilayah')

        try:
            with transaction.atomic():
                
                
                # Hitung jumlah penduduk
                jumlah_penduduk = pria + wanita
                data_penduduk = Data_peduduk.objects.create(
                    identitas=identitas,
                    pria=pria,
                    wanita=wanita,
                    jumlah_kk=jumlah_kk,
                    jumlah_penduduk=jumlah_penduduk,
                    wilayah=MasterWilayah.objects.get(wilayah_id=wilayah_id),
                    created_at=timezone.now()
                )
                data_penduduk.save()
                

                messages.success(request, "Data penduduk berhasil ditambahkan.")
                return redirect('admin_setori:data_penduduk')

        except Exception as e:
            print("Error:", e)
            messages.error(request, "Gagal menambahkan data penduduk.")
            return redirect('admin_setori:data_penduduk')
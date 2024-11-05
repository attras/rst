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
        
        dt_data_penduduk = Data_peduduk.objects.select_related('wilayah').filter(deleted_at__isnull=True)
        pilih_wilayah = MasterWilayah.objects.filter(deleted_at__isnull=True, wilayah_level=4)
        # total_pria = Data_peduduk.objects.aggregate(total_pria=Sum('pria'))['total_pria'] or 0
        total_pria_per_wilayah = (
            Data_peduduk.objects
            .filter(deleted_at__isnull=True)  # Pastikan untuk menghindari data yang dihapus
            .values('wilayah__wilayah_nama')  # Mengelompokkan berdasarkan nama wilayah
            .annotate(
                        total_pria=Sum('pria'),  # Menghitung total pria untuk setiap wilayah
                        total_wanita=Sum('wanita')  # Menghitung total wanita untuk setiap wilayah
                    ))
        
      
        total_pria_per_wilayah_parent = (
            Data_peduduk.objects
            .filter(deleted_at__isnull=True)  # Pastikan untuk menghindari data yang dihapus
            .values('wilayah__wilayah_parent__wilayah_nama')  # Mengelompokkan berdasarkan nama wilayah_parent
            .annotate(total_pria=Sum('pria'))  # Menghitung total pria untuk setiap wilayah_parent
        )

        total_pria = Data_peduduk.objects.filter(deleted_at__isnull=True).aggregate(total_pria=Sum('pria'))['total_pria']



        data = {
            'dt_data_penduduk' : dt_data_penduduk,
            'pilih_wilayah' : pilih_wilayah,
            'identitas_choices': IDENTITAS_CHOICE,
            'total_pria_per_wilayah': total_pria_per_wilayah,
            'total_pria_per_wilayah_parent': total_pria_per_wilayah_parent,
            'total_pria': total_pria,
 
        }
       
        return render(request, 'admin/admin_data_penduduk/index.html',data)

class Add_data_penduduk(View):
    def post(self, request):
        identitas_oap = request.POST.get('identitas-oap')
        identitas_non = request.POST.get('identitas-non')
        pria_oap = int(request.POST.get('pria-oap', 0))
        wanita_oap = int(request.POST.get('wanita-oap', 0))
        kk_oap = int(request.POST.get('kk-oap', 0))

        pria = int(request.POST.get('pria-non', 0))
        wanita = int(request.POST.get('wanita-non', 0))
        kk_non = int(request.POST.get('kk-non', 0))
        wilayah_id = request.POST.get('wilayah')

        existing_entry = Data_peduduk.objects.filter(wilayah_id=wilayah_id, identitas=identitas_non or identitas_oap).first()

        if existing_entry:
            messages.error(request, "Data dengan kombinasi wilayah dan identitas ini sudah ada.")
            return redirect('admin_setori:data_penduduk')
        
        try:
            with transaction.atomic():
                
                
                # Hitung jumlah penduduk
                jumlah_penduduk = pria + wanita
                data_penduduk = Data_peduduk.objects.create(
                    identitas='1',
                    pria=pria_oap,
                    wanita=wanita_oap,
                    jumlah_kk=kk_oap,
                    jumlah_penduduk=jumlah_penduduk,
                    wilayah=MasterWilayah.objects.get(wilayah_id=wilayah_id),
                    created_at=timezone.now()
                )
                data_penduduk.save()

                jumlah_penduduk = pria + wanita
                data_penduduk = Data_peduduk.objects.create(
                    identitas='2',
                    pria=pria,
                    wanita=wanita,
                    jumlah_kk=kk_non,
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
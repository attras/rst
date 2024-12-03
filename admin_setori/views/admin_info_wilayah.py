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
        breadcrump = [{
        'nama': 'Data Penduduk',
        'url': reverse('admin_setori:data_penduduk'),
        }
        ]
        dt_wilayah = MasterWilayah.objects.filter(deleted_at__isnull=True).order_by('wilayah_level')

        data = {
            'dt_wilayah': dt_wilayah,
            'LEVEL_WILAYAH': LEVEL_WILAYAH,
            'breadcrump': breadcrump,
            'title':'Data Penduduk'

            
        }

        return render(request, 'admin/admin_info_wilayah/index.html',data)

class Detail_info_wilayah(View):
    def get(self, request,wilayah_id):
        breadcrump = [{
        'nama': 'Info Wilayah',
        'url': reverse('admin_setori:admin_info_wilayah'),
        },
        {
        'nama': 'Detail Info Wilayah',
        'url': reverse('admin_setori:detail_info_wilayah',args=[wilayah_id]),
        }
        ]


        dt_info_wilayah = Info_wilayah.objects.filter(deleted_at__isnull = True,wilayah_id=wilayah_id)
        pilih_wilayah = MasterWilayah.objects.filter(deleted_at__isnull = True,wilayah_id=wilayah_id)
        dt_sarpras = Data_sarpras.objects.filter(deleted_at__isnull = True,wilayah=wilayah_id)
       
        try:
            data_info_wilayah =  Info_wilayah.objects.get(wilayah_id=wilayah_id, deleted_at__isnull=True)
        # Jika ada data penduduk, ambil semua field
        except ObjectDoesNotExist:
            data_info_wilayah = None  # Atau menangani error sesuai kebutuhan

        used_sarpras = Data_sarpras.objects.filter(deleted_at__isnull = True,wilayah=wilayah_id).values_list('nama_sarpras', flat=True)
        available_sarpras = Master_sarpras.objects.exclude(pk__in=  used_sarpras)
        data = {
            'available_sarpras': available_sarpras,
            'dt_info_wilayah' : dt_info_wilayah,
            'pilih_wilayah' : pilih_wilayah,
            'wilayah_id' : wilayah_id,
            'data_info_wilayah' : data_info_wilayah,
            'dt_sarpras' : dt_sarpras,
            'breadcrump': breadcrump,
            'title' : 'Detail Info Wilayah'

        }
        
        return render(request, 'admin/admin_info_wilayah/detail.html',data)
    



class FormWilayah(View):
    def get(self, request,wilayah_id):
        breadcrump = [{
        'nama': 'Info Wilayah',
        'url': reverse('admin_setori:admin_info_wilayah'),
        },
        {
        'nama': 'Detail Info Wilayah',
        'url': reverse('admin_setori:detail_info_wilayah',args=[wilayah_id]),
        },
        {
        'nama': 'Form Info Wilayah',
        'url': reverse('admin_setori:detail_info_wilayah',args=[wilayah_id]),
        }
        ]

        dt_info_wilayah = Info_wilayah.objects.filter(deleted_at__isnull = True,wilayah_id=wilayah_id)
        pilih_wilayah = MasterWilayah.objects.filter(deleted_at__isnull = True,wilayah_id=wilayah_id).first()
        data = {
            'dt_info_wilayah' : dt_info_wilayah,
            'pilih_wilayah' : pilih_wilayah,
            'wilayah_id' : wilayah_id,
            'breadcrump': breadcrump,
            'title' : 'Form Info Wilayah'
       
        }
        
        return render(request, 'admin/admin_info_wilayah/form.html',data)


class Addsarpras(View):
    def post(self, request):
        wilayah_id = request.POST.get('wilayah_id')
        nama_sarpras = request.POST.get('nama_sarpras')
        jumlah_sarpras = request.POST.get('jumlah')

        try:
            with transaction.atomic():
                sarpras_id = Master_sarpras.objects.get(pk=nama_sarpras)
                wilayah = MasterWilayah.objects.get(pk=wilayah_id)
                sarpras = Data_sarpras()
                sarpras.nama_sarpras= sarpras_id
                sarpras.jumlah = jumlah_sarpras
                sarpras.wilayah= wilayah
            
                sarpras.save()


                messages.success(request, "Data sarpras berhasil ditambahkan.")
                return redirect('admin_setori:detail_info_wilayah', wilayah_id)  # Ubah dengan nama URL yang sesuai

        except Exception as e:
                print("Error Data:", e)
                messages.error(request, "Gagal menambahkan data sarpras.")
                return redirect('admin_setori:admin_info_wilayah',wilayah_id)  # Ubah dengan nama URL yang sesuai




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
        
class EditInfoWilayah(View):
     def get(self, request,wilayah_id):
        dt_info_wilayah = Info_wilayah.objects.filter(deleted_at__isnull = True,wilayah_id=wilayah_id)
        pilih_wilayah = MasterWilayah.objects.filter(deleted_at__isnull = True,wilayah_id=wilayah_id).first()
        info_wilayah = get_object_or_404(Info_wilayah,  wilayah_id=wilayah_id, deleted_at__isnull=True)
               
        data = {
            'dt_info_wilayah' : dt_info_wilayah,
            'pilih_wilayah' : pilih_wilayah,
            'wilayah_id' : wilayah_id,
            'info_wilayah' : info_wilayah,
            'edit':True,
       
        }
        
        return render(request, 'admin/admin_info_wilayah/form.html',data)
     
     def post(self, request,wilayah_id):
        dt_wilayah = get_object_or_404(Info_wilayah,  wilayah_id=wilayah_id, deleted_at__isnull=True)
                
        visi = request.POST.get('visi')
        misi = request.POST.get('misi')
        kode_info_wilayah = request.POST.get('kode_info_wilayah')
        tahun_pembentukan = request.POST.get('tahun_pembentukan')
        kode_pos = request.POST.get('kode_pos')
        link_maps = request.POST.get('map')
        image_profile = request.FILES.get('profil') or dt_wilayah.image_profile
       
        try:
            with transaction.atomic():
                

                info_wilayah = get_object_or_404(Info_wilayah,  wilayah_id=wilayah_id, deleted_at__isnull=True)
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
       


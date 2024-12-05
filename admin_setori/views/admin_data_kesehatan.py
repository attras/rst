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
class Admin_data_kesehatanViews(View):
    def get(self, request):
        breadcrump = [{
        'nama': 'Data',
        'url': reverse('admin_setori:data_kesehatan'),
        }
        ]
        dt_kesehatan = Master_jenis_kesehatan.objects.filter(deleted_at__isnull = True)

        data = {
            'dt_kesehatan': dt_kesehatan,
            'breadcrump': breadcrump,
            'title' : 'Data'
        }
        
      
        return render(request, 'admin/data_kesehatan/index.html',data)
    
class Detail_data_kesehatanViews(View):
    def get(self,request,jenis_kesehatan_id):
        breadcrump = [{
            'nama' : 'Data Kesehatan',
            'url' : reverse('admin_setori:data_kesehatan')
        },
        {
        'nama': 'Pilih wilayah',
        'url': reverse('admin_setori:detail_data_kesehatan',args=[jenis_kesehatan_id])
        }
        ]

        dt_kesehatan = Data_kesehatan.objects.filter(deleted_at__isnull = True,fk_jenis=jenis_kesehatan_id)
        jenis_kesehatan = Master_jenis_kesehatan.objects.filter(deleted_at__isnull = True,jenis_kesehatan_id=jenis_kesehatan_id)
        dt_indikator = Indikator_kesehatan.objects.filter(deleted_at__isnull = True,jenis_kesehatan_id=jenis_kesehatan_id)
        dt_wilayah = MasterWilayah.objects.filter(deleted_at__isnull = True,wilayah_level='4')
        data = {
            'dt_indikator': dt_indikator,
            'jenis_kesehatan': jenis_kesehatan,
            'dt_wilayah': dt_wilayah,
            'dt_kesehatan': dt_kesehatan,
            'jenis_kesehatan_id' : jenis_kesehatan_id,
            'breadcrump': breadcrump,
            'title' : 'Pilih wilayah',
            'jenis_kesehatan_id' : jenis_kesehatan_id
        }
        

        return render(request,'admin/data_kesehatan/pilih_wilayah.html',data)

class xDetail_data_kesehatanViews(View):
    def get(self,request,jenis_kesehatan_id,wilayah_id):
        breadcrump = [{
            'nama' : 'Data Kesehatan',
            'url' : reverse('admin_setori:data_kesehatan')
        },
        {
        'nama': 'Pilih wilayah',
        'url': reverse('admin_setori:detail_data_kesehatan',args=[jenis_kesehatan_id])
        },
         {
        'nama': 'Input data',
        'url': reverse('admin_setori:xdetail_data_kesehatan',args=[jenis_kesehatan_id,wilayah_id])
        }
       
        ]

        
        # dt_kesehatan = Data_kesehatan.objects.filter(deleted_at__isnull = True,fk_jenis=jenis_kesehatan_id,wilayah=wilayah_id)
        jenis_kesehatan = Master_jenis_kesehatan.objects.filter(deleted_at__isnull = True,jenis_kesehatan_id=jenis_kesehatan_id)
        dt_kesehatan = Data_kesehatan.objects.filter(deleted_at__isnull = True,fk_jenis=jenis_kesehatan_id,wilayah_id=wilayah_id).select_related('indikator', 'fk_jenis')
        used_indikator =  Data_kesehatan.objects.filter(deleted_at__isnull = True,fk_jenis=jenis_kesehatan_id,wilayah_id=wilayah_id).values_list('indikator', flat=True)
        print(used_indikator)
    # Ambil semua indikator terkait dengan fk_jenis yang ada di data_kesehatan
        dt_indikator = Indikator_kesehatan.objects.filter(deleted_at__isnull = True,jenis_kesehatan_id=jenis_kesehatan_id).exclude(id_indikator__in=used_indikator)
       
        wilayah_list = MasterWilayah.objects.filter(deleted_at__isnull = True,wilayah_level='4',wilayah_id=wilayah_id)
        data = {
            'dt_indikator': dt_indikator,
            'jenis_kesehatan': jenis_kesehatan,
            'wilayah_list': wilayah_list,
            'dt_kesehatan': dt_kesehatan,
            'jenis_kesehatan_id' : jenis_kesehatan_id,
            'breadcrump': breadcrump,
            'jenis_kesehatan_id':jenis_kesehatan_id,
            'title' : 'Input Data'
        }
        

        return render(request,'admin/data_kesehatan/detail.html',data)
    
class Add_data_kesehatan(View) :
    def post(self, request):
        fk_jenis_id = request.POST.get('jenis_kesehatan')
        wilayah_id = request.POST.get('wilayah')
        indikator_id = request.POST.get('indikator')
        oap = request.POST.get('oap')
        non_oap = request.POST.get('non_oap')

        wilayah = MasterWilayah.objects.get(wilayah_id=wilayah_id)
        fk_jenis = Master_jenis_kesehatan.objects.get(jenis_kesehatan_id=fk_jenis_id)
        indikator = Indikator_kesehatan.objects.get(id_indikator=indikator_id)

        try:
            with transaction.atomic():
                input_kesehatan = Data_kesehatan(
                    wilayah = wilayah,
                    fk_jenis = fk_jenis,
                    indikator = indikator,
                    oap = oap,
                    non_oap = non_oap,
                )
               
                input_kesehatan.save()
                

                messages.success(request, f"data berhasil Ditambahkan")
                return redirect('admin_setori:xdetail_data_kesehatan',jenis_kesehatan_id=fk_jenis_id, wilayah_id= wilayah_id)
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal menambahkan")
            return redirect('admin_setori:xdetail_data_kesehatan',jenis_kesehatan_id=fk_jenis_id, wilayah_id= wilayah_id)


class DeleteKesehatan(View):
    def get(self, request, data_kesehatan_id):
        del_kesehatan = get_object_or_404(Data_kesehatan, data_kesehatan_id=data_kesehatan_id)
        
        try:
            with transaction.atomic():
                del_kesehatan.delete()
                messages.success(request, "Data berhasil dihapus")
        except Exception as e:
            print('Error Data:', e)
            messages.error(request, "Gagal menghapus data")
        
        return redirect("admin_setori:data_kesehatan")


class Delete_at_kesehatan(View):
    def get(self,request,data_kesehatan_id):
        try:
            with transaction.atomic():
                del_kesehatan = get_object_or_404(Data_kesehatan, data_kesehatan_id=data_kesehatan_id)
                del_kesehatan.deleted_at = timezone.now()
                del_kesehatan.save()
                messages.success(request, f"data berhasil dihapus")
                return redirect('admin_setori:data_kesehatan')
                
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal menghapus")
            return redirect('admin_setori:data_kesehatan')


class Historikesehatan(View):
    def get(self,request):
        dt_kesehatan = Data_kesehatan.objects.filter(deleted_at__isnull = False)
        jenis_kesehatan = Master_jenis_kesehatan.objects.filter(deleted_at__isnull = False)
        dt_indikator = Indikator_kesehatan.objects.filter(deleted_at__isnull = False)
        wilayah_list = MasterWilayah.objects.filter(deleted_at__isnull = False,wilayah_level='4')
        breadcrump = [{
            'nama' : 'Data Kesehatan',
            'url' : reverse('admin_setori:data_kesehatan')
        }
        
       
        ]
        data = {
            'dt_indikator': dt_indikator,
            'jenis_kesehatan': jenis_kesehatan,
            'wilayah_list': wilayah_list,
            'dt_kesehatan': dt_kesehatan,
            'breadcrump': breadcrump,
            'title':'Riwayat Master slider'
        }
        return render(request,'admin/data_kesehatan/histori.html',data)
    
class Restorekesehatan(View):
    def get(self, request, data_kesehatan_id):
        try:
            with transaction.atomic():
                del_kesehatan = get_object_or_404(Data_kesehatan,data_kesehatan_id=data_kesehatan_id)
                del_kesehatan.deleted_at = None
                del_kesehatan.save()
                messages.success(request, f"data berhasil dipulihkan")
                return redirect('admin_setori:histori_kesehatan')
                
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal menghapus")
            return redirect('admin_setori:histori_kesehatan')

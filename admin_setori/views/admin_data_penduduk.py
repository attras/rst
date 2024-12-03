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
from django.core.exceptions import ObjectDoesNotExist

@method_decorator(login_required(), name='dispatch')
class Admin_data_pendudukViews(View):
    def get(self, request):
        breadcrump = [{
        'nama': 'Data Penduduk',
        'url': reverse('admin_setori:data_penduduk'),
        }
        ]
        dt_wilayah = MasterWilayah.objects.filter(deleted_at__isnull=True,wilayah_level='4').order_by('wilayah_level')

        data = {
            'dt_wilayah': dt_wilayah,
            'LEVEL_WILAYAH': LEVEL_WILAYAH,
            'breadcrump': breadcrump,
            'title':'Data Penduduk'
            
        }
        

        return render(request, 'admin/admin_data_penduduk/index.html',data)
    
class Semua_data(View):
    def get(self, request):
        breadcrump = [{
        'nama': 'Data Penduduk',
        'url': reverse('admin_setori:data_penduduk'),
        }
        ]
        wilayah_list = MasterWilayah.objects.filter(deleted_at__isnull = True)
        dt_penduduk = Data_penduduk.objects.filter(deleted_at__isnull = True)
        
        used_wilayah = Data_penduduk.objects.values_list('wilayah_id', flat=True)
        wilayah = MasterWilayah.objects.filter(
            deleted_at__isnull=True,
            wilayah_level='4'  # Filter level wilayah = 4
        ).exclude(wilayah_id__in=used_wilayah).order_by('wilayah_nama')

        # fungsi tambah
      
        data = (
            Data_penduduk.objects
            .values('wilayah__wilayah_parent__wilayah_nama')
            .annotate(total_pria_oap=Sum('pria_oap'),
                      total_pria_non_oap=Sum('pria_non_oap'),
                      total_wanita_oap=Sum('wanita_oap'),
                      total_wanita_non_oap=Sum('wanita_non_oap'),
                      total_jumlah_kk_oap=Sum('jumlah_kk_oap'),
                      total_jumlah_kk_non_oap=Sum('jumlah_kk_non_oap'),
                      )
            .order_by('wilayah__wilayah_parent__wilayah_nama')
        )

        # Mengambil wilayah yang memiliki level '4' untuk digunakan dalam dropdown
        dt_wilayah = MasterWilayah.objects.filter(deleted_at__isnull=True, wilayah_level='4').order_by('wilayah_level')

        # for item in data:
        #     parent_name = item['wilayah__wilayah_parent__wilayah_nama']
           
        #     # Mendapatkan wilayah parent berdasarkan nama wilayah parent
        #     wilayah_parent = MasterWilayah.objects.filter(wilayah_nama=parent_name).first()
            
        #     if not wilayah_parent:
        #         print(f"Wilayah parent '{parent_name}' tidak ditemukan.")
        #         continue  # Lewati jika wilayah parent tidak ditemukan

        #     # Cek apakah sudah ada data untuk wilayah yang sama
        #     existing_data = Data_penduduk.objects.filter(wilayah=wilayah_parent).exists()

        #     if not existing_data:
        #         # Membuat entri baru di Data_penduduk jika belum ada data untuk wilayah tersebut
        #         Data_penduduk.objects.create(
        #             wilayah=wilayah_parent,
        #             pria_oap=item['total_pria_oap'] or 0,
        #             pria_non_oap=item['total_pria_non_oap'] or 0,  # Menambahkan nilai sesuai dengan kebutuhan
        #             wanita_oap=item['total_wanita_oap'] or 0,    # Menambahkan nilai sesuai dengan kebutuhan
        #             wanita_non_oap=item['total_wanita_non_oap']or 0, # Menambahkan nilai sesuai dengan kebutuhan
        #             jumlah_kk_oap=item['total_jumlah_kk_oap'] or 0,
        #             jumlah_kk_non_oap=item['total_jumlah_kk_non_oap']or 0
        #      )
               
        #     else:
                
        #         data_penduduk = Data_penduduk.objects.get(wilayah=wilayah_parent)
        #         data_penduduk.pria_oap = item['total_pria_oap'] or 0
        #         data_penduduk.pria_non_oap = item['total_pria_non_oap'] or 0  # Menambahkan nilai sesuai dengan kebutuhan
        #         data_penduduk.wanita_oap = item['total_wanita_oap'] or 0    # Menambahkan nilai sesuai dengan kebutuhan
        #         data_penduduk.wanita_non_oap = item['total_wanita_non_oap']or 0  # Menambahkan nilai sesuai dengan kebutuhan
        #         data_penduduk.jumlah_kk_oap = item['total_jumlah_kk_oap'] or 0 # Menambahkan nilai sesuai dengan kebutuhan
        #         data_penduduk.jumlah_kk_non_oap = item['total_jumlah_kk_non_oap']or 0  # Menambahkan nilai sesuai dengan kebutuhan
        #         data_penduduk.save()
        #         print("update")
               
        # end fungsi tambah

        contex={
            'dt_penduduk': dt_penduduk,
            'wilayah_list': wilayah_list,
            'wilayah': wilayah,
            'data': data,
            'dt_wilayah': dt_wilayah,
            'breadcrump': breadcrump,
            'title':'Data Penduduk'

         
        }

        return render(request,'admin/admin_data_penduduk/semua.html',contex)
    
class Detail_penduduk(View):
    def get(self, request,wilayah_id):
        wilayah_list = MasterWilayah.objects.filter(deleted_at__isnull = True,wilayah_id=wilayah_id)
        dt_penduduk = Data_penduduk.objects.filter(deleted_at__isnull = True,wilayah=wilayah_id)
        try:
            data_penduduk = Data_penduduk.objects.get(wilayah=wilayah_id, deleted_at__isnull=True)
        # Jika ada data penduduk, ambil semua field
        except ObjectDoesNotExist:
            data_penduduk = None  # Atau menangani error sesuai kebutuhan


       


        data={
            'dt_penduduk': dt_penduduk,
            'wilayah_list': wilayah_list,
            'data_penduduk':data_penduduk,
            
        }

        return render(request,'admin/admin_data_penduduk/detail.html',data)
    

class Add_data_penduduk(View):
    def post(self, request):
        wilayah_id = request.POST.get("wilayah")
         # Cek apakah wilayah sudah ada di model Data_penduduk
        if Data_penduduk.objects.filter(wilayah_id=wilayah_id).exists():
            messages.error(request, "Data untuk wilayah ini sudah ada.")
            return redirect("admin_setori:detail_data_penduduk",wilayah_id=wilayah_id)
        
        pria_oap = int(request.POST.get("pria_oap", 0))
        pria_non_oap = int(request.POST.get("pria_non_oap", 0))
        wanita_oap = int(request.POST.get("wanita_oap", 0))
        wanita_non_oap = int(request.POST.get("wanita_non_oap", 0))
        jumlah_kk_oap = int(request.POST.get("jumlah_kk_oap", 0))
        jumlah_kk_non_oap = int(request.POST.get("jumlah_kk_non_oap", 0))

        # Dapatkan objek wilayah
        wilayah = get_object_or_404(MasterWilayah, deleted_at__isnull=True, wilayah_id=wilayah_id)

        # Ambil parent dari wilayah yang dimaksud
        parent_wilayah_id = wilayah.wilayah_parent.wilayah_id if wilayah.wilayah_parent else None

        
        try:
            with transaction.atomic():
                
                data_penduduk = Data_penduduk(
                    wilayah_id=wilayah_id,
                    pria_oap=pria_oap,
                    pria_non_oap=pria_non_oap,
                    wanita_oap=wanita_oap,
                    wanita_non_oap=wanita_non_oap,
                    jumlah_kk_oap=jumlah_kk_oap,
                    jumlah_kk_non_oap=jumlah_kk_non_oap
                )
                data_penduduk.save()

                if parent_wilayah_id and Data_penduduk.objects.filter(wilayah_id=parent_wilayah_id).exists():
                  
                    print("data_sudah ada")
                else:
                    print(parent_wilayah_id)
                    print("anjay mabar")  # Cetak pesan jika data sudah ada tetapi tetap melanjutkan eksekusi
            
               

                
                messages.success(request, "Data penduduk berhasil ditambahkan.")
                return redirect("admin_setori:semua_penduduk")  # Kembali ke form jika berhasil
            
        except Exception as e:
            print("Gagal menambahkan data:", e)
            messages.error(request, "Gagal menambahkan data penduduk.")
            return redirect("admin_setori:semua_penduduk")  # Kembali ke form jika gagal


class edit_data_penduduk(View):
    def post(self, request,data_penduduk_id):
        wilayah_id = request.POST.get("wilayah")
        pria_oap = int(request.POST.get("pria_oap", 0))
        pria_non_oap = int(request.POST.get("pria_non_oap", 0))
        wanita_oap = int(request.POST.get("wanita_oap", 0))
        wanita_non_oap = int(request.POST.get("wanita_non_oap", 0))
        jumlah_kk_oap = int(request.POST.get("jumlah_kk_oap", 0))
        jumlah_kk_non_oap = int(request.POST.get("jumlah_kk_non_oap", 0))

        try:
            with transaction.atomic():
                data_penduduk =  get_object_or_404(Data_penduduk,data_penduduk_id=data_penduduk_id)
                data_penduduk.pria_oap=pria_oap
                data_penduduk.pria_non_oap=pria_non_oap
                data_penduduk.wanita_oap=wanita_oap
                data_penduduk.wanita_non_oap=wanita_non_oap
                data_penduduk.jumlah_kk_oap=jumlah_kk_oap
                data_penduduk.jumlah_kk_non_oap=jumlah_kk_non_oap
                
                data_penduduk.save()

                

                messages.success(request, "Data penduduk berhasil diedit.")
                return redirect("admin_setori:detail_data_penduduk",wilayah_id=wilayah_id)  # Kembali ke form jika gagal
  # Kembali ke form jika berhasil
            
        except Exception as e:
            print("Gagal menambahkan data:", e)
            messages.error(request, "Gagal mengedit data penduduk.")
            return redirect("admin_setori:detail_data_penduduk",wilayah_id=wilayah_id)  # Kembali ke form jika gagal


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
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
class Admin_tetang_kami(View):
    def get(self, request):
        dt_tentang = Tentang.objects.filter(deleted_at__isnull = True)
        data = {
            'dt_tentang' : dt_tentang,
        }
        return render(request, 'admin/admin_tentang/index.html', data)

class Add_tentang(View):
    def get(self, request):
        dt_tentang = Tentang.objects.filter(deleted_at__isnull = True)
        data = {
            'dt_tentang' : dt_tentang,
        }
        return render(request, 'admin/admin_tentang/form.html', data)

    def post(self, request):
        pengantar_tentang = request.POST.get('pengantar_tentang')
        nama_kepala = request.POST.get('nama_kepala')
        jabatan_kepala = request.POST.get('jabatan_kepala')
        nama_sekretaris = request.POST.get('nama_sekretaris')
        jabatan_sekretaris = request.POST.get('jabatan_sekretaris')
        deskripsi_singkat_tentang = request.POST.get('deskripsi_singkat_tentang')
        kata_kepala = request.POST.get('kata_kepala')
        kata_sekretaris = request.POST.get('kata_sekretaris')

        foto_kepala = request.FILES.get('foto_kepala')
        foto_sekretaris = request.FILES.get('foto_sekretaris')
        thumbnail_profil = request.FILES.get('thumbnail_profil')

        try :
            with transaction.atomic():
                insert_tentang = Tentang()
                insert_tentang.pengantar = pengantar_tentang
                insert_tentang.foto_pegantar = thumbnail_profil
                insert_tentang.nama_kepala_dinas = nama_kepala
                insert_tentang.jabatan_kepala = jabatan_kepala
                insert_tentang.nama_sekretaris = nama_sekretaris
                insert_tentang.jabatan_sekretaris = jabatan_sekretaris
                insert_tentang.deskripsi_singkat = deskripsi_singkat_tentang
                insert_tentang.foto_kepala = foto_kepala
                insert_tentang.foto_sekretaris = foto_sekretaris
                insert_tentang.kata_kepala = kata_kepala
                insert_tentang.kata_sekretaris = kata_sekretaris
                insert_tentang.save()
                messages.success(request, " added successfully!")
                return redirect('admin_setori:admin_tentang') 

        except Exception as e:
            print('Error while adding category', e)
            messages.error(request, "Failed to add ")
            return redirect('admin_setori:admin_tentang')


class Edittentang(View):
    def get(self, request, id_tentang):
        dt_tentang = get_object_or_404(Tentang, id_tentang=id_tentang)
        data = {
            'dt_tentang' : dt_tentang,
            'edit' : True,
            'id_tentang' : id_tentang,
        }
        return render(request, 'admin/admin_tentang/form.html', data)

    def post(self, request, id_tentang):
        pengantar_tentang = request.POST.get('pengantar_tentang')
        nama_kepala = request.POST.get('nama_kepala')
        jabatan_kepala = request.POST.get('jabatan_kepala')
        nama_sekretaris = request.POST.get('nama_sekretaris')
        jabatan_sekretaris = request.POST.get('jabatan_sekretaris')
        deskripsi_singkat_tentang = request.POST.get('deskripsi_singkat_tentang')
        kata_kepala = request.POST.get('kata_kepala')
        kata_sekretaris = request.POST.get('kata_sekretaris')

        foto_kepala = request.FILES.get('foto_kepala')
        foto_sekretaris = request.FILES.get('foto_sekretaris')
        thumbnail_profil = request.FILES.get('thumbnail_profil')

        try :
            with transaction.atomic():
                insert_tentang = get_object_or_404(Tentang, id_tentang=id_tentang)
                insert_tentang.pengantar = pengantar_tentang
                insert_tentang.foto_pegantar = thumbnail_profil
                insert_tentang.nama_kepala_dinas = nama_kepala
                insert_tentang.jabatan_kepala = jabatan_kepala
                insert_tentang.nama_sekretaris = nama_sekretaris
                insert_tentang.jabatan_sekretaris = jabatan_sekretaris
                insert_tentang.deskripsi_singkat = deskripsi_singkat_tentang
                insert_tentang.foto_kepala = foto_kepala
                insert_tentang.foto_sekretaris = foto_sekretaris
                insert_tentang.kata_kepala = kata_kepala
                insert_tentang.kata_sekretaris = kata_sekretaris
                insert_tentang.save()

                messages.success(request, f"data berhasil Ditambahkan")
                return redirect('admin_setori:admin_tentang') 

        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal menambahkan")
            return redirect('admin_setori:admin_tentang') 
 
class Deletetentang(View):
    def get(self, request, id_tentang):
        del_tentang = get_object_or_404(Tentang, id_tentang=id_tentang)
        del_tentang.delete()
        messages.success(request, f"data berhasil dihapus")
        return redirect('admin_setori:admin_tentang')
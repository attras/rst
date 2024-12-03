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
class LayananViews(View):
    def get(self, request):
        breadcrump = [{
        'nama': 'Layanan',
        'url': reverse('admin_setori:admin_layanan'),
        }
        ]
        dt_layanan = Layanan.objects.filter(deleted_at__isnull = True)
        data = {
            'title' : 'Layanan',
            'dt_layanan' : dt_layanan,
            'breadcrump' : breadcrump,
            'title' : 'Layanan'
        }
        return render(request, 'admin/admin_layanan/index.html',data)

class Addlayanan(View) :
    def get(self, request):
        breadcrump = [{
            'nama': 'Layanan',
            'url': reverse('admin_setori:admin_layanan'),
        },{
            'nama': 'Tambah Layanan',
            'url': reverse('admin_setori:add_layanan'),
        }
        ]
        dt_layanan = Layanan.objects.filter(deleted_at__isnull = True)
        data = {
            'title' : 'Tambah data',
            'dt_layanan' : dt_layanan,
            'breadcrump' : breadcrump,
            'title' : 'Tambah Layanan'
        }
        return render(request, 'admin/admin_layanan/form.html',data)

    def post(self, request):
        surat = request.POST.get('surat')
        syarat = request.POST.get('syarat')
        try:
            with transaction.atomic():
                insert_layanan = Layanan()
                insert_layanan.surat = surat
                insert_layanan.syarat = syarat
                insert_layanan.created_at = timezone.now()
                insert_layanan.save()

                messages.success(request, f"data berhasil Ditambahkan")
                return redirect('admin_setori:admin_layanan')
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal menambahkan")
            return redirect('admin_setori:admin_layanan')
        
class Deletelayanan(View):
    def get(self, request, id_layanan):
        del_layanan = get_object_or_404(Layanan,id_layanan=id_layanan)
        del_layanan.delete()
        messages.success(request, f"data berhasil dihapus")
        return redirect('admin_setori:histori_layanan')
    

class Editlayanan(View) :
    def get(self, request,id_layanan):
        breadcrump = [{
            'nama': 'Layanan',
            'url': reverse('admin_setori:admin_layanan'),
        },{
            'nama': 'Edit Layanan',
            'url': reverse('admin_setori:edit_layanan',args=[id_layanan]),
        }
        ]

        dt_layanan = get_object_or_404(Layanan, id_layanan=id_layanan,deleted_at__isnull = True )
        data = {
            'title' : 'edit ',
            'edit': True,
            'dt_layanan' : dt_layanan,
            'breadcrump' : breadcrump,
            'title' : 'Edit Layanan'
        }
        return render(request, 'admin/admin_layanan/form.html',data)

    def post(self, request,id_layanan):
        surat = request.POST.get('surat')
        syarat = request.POST.get('syarat')
        try:
            with transaction.atomic():
                insert_layanan = get_object_or_404(Layanan, id_layanan=id_layanan,deleted_at__isnull = True )
                insert_layanan.surat = surat
                insert_layanan.syarat = syarat
                insert_layanan.save()

                messages.success(request, f"data berhasil diedit")
                return redirect('admin_setori:admin_layanan')
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal edit")
            return redirect('admin_setori:admin_layanan')


class Delete_at(View):
    def get(self, request, id_layanan):
        try:
            with transaction.atomic():
                del_layanan = get_object_or_404(Layanan,id_layanan=id_layanan)
                del_layanan.deleted_at = timezone.now()
                del_layanan.save()
                messages.success(request, f"data berhasil dihapus")
                return redirect('admin_setori:admin_layanan')
                
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal menghapus")
            return redirect('admin_setori:admin_layanan')


class Historilayanan(View):
    def get(self, request):
        dt_layanan = Layanan.objects.filter(deleted_at__isnull = False)
        data = {
            'dt_layanan' : dt_layanan
        }
        return render(request, 'admin/admin_layanan/histori.html',data)
    
class Restorelayanan(View):
    def get(self, request, id_layanan):
        try:
            with transaction.atomic():
                del_layanan = get_object_or_404(Layanan,id_layanan=id_layanan)
                del_layanan.deleted_at = None
                del_layanan.save()
                messages.success(request, f"data berhasil dipulihkan")
                return redirect('admin_setori:histori_layanan')
                
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal menghapus")
            return redirect('admin_setori:histori_layanan')
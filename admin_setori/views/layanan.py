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
        dt_layanan = Layanan.objects.filter(deleted_at__isnull = True)
        data = {
            'dt_layanan' : dt_layanan
        }
        return render(request, 'admin/layanan.html',data)

class Addlayanan(View) :
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
    def get(self, request, layanan_id):
        del_layanan = get_object_or_404(Layanan,id_layanan=layanan_id)
        del_layanan.delete()
        messages.success(request, f"data berhasil dihapus")
        return redirect('admin_setori:admin_layanan')

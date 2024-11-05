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
class Admin_kontakViews(View):
    def get(self, request):
        dt_kontak = Kontak.objects.filter(deleted_at__isnull = True)
        data = {
            'dt_kontak' : dt_kontak
        }
        return render(request, 'admin/admin_kontak/index.html',data)
    
class Addkontak(View):
    def post(self, request):
        nama_instansi = request.POST.get('nama_instansi')
        maps = request.POST.get('maps')
        link_ig = request.POST.get('link_ig')
        link_twitter = request.POST.get('link_twitter')
        link_facebook = request.POST.get('link_facebook')
        no_pengaduan = request.POST.get('no_pengaduan')
        alamat = request.POST.get('alamat')
        email_pengaduan = request.POST.get('email_pengaduan')
        email_cs = request.POST.get('email_cs')

        try:
            with transaction.atomic():
                insert_kontak = Kontak()
                insert_kontak.nama_instansi = nama_instansi
                insert_kontak.maps = maps  
                insert_kontak.link_ig = link_ig
                insert_kontak.link_twitter = link_twitter
                insert_kontak.link_facebook = link_facebook
                insert_kontak.no_pengaduan = no_pengaduan
                insert_kontak.alamat = alamat
                insert_kontak.email_pengaduan = email_pengaduan
                insert_kontak.email_cs = email_cs
                insert_kontak.created_at = timezone.now()
                insert_kontak.save()

                messages.success(request, f"data berhasil Ditambahkan")
                return redirect('admin_setori:admin_kontak')
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal menambahkan")
            return redirect('admin_setori:admin_kontak')

class Editkontak(View):
    def post(self, request):
        nama_instansi = request.POST.get('nama_instansi')
        maps = request.POST.get('maps')
        link_ig = request.POST.get('link_ig')
        link_twitter = request.POST.get('link_twitter')
        link_facebook = request.POST.get('link_facebook')
        no_pengaduan = request.POST.get('no_pengaduan')
        alamat = request.POST.get('alamat')
        email_pengaduan = request.POST.get('email_pengaduan')
        email_cs = request.POST.get('email_cs')

        try:
            with transaction.atomic():
                insert_kontak = get_object_or_404(Kontak, id=id)
                insert_kontak.nama_instansi = nama_instansi
                insert_kontak.maps = maps  
                insert_kontak.link_ig = link_ig
                insert_kontak.link_twitter = link_twitter
                insert_kontak.link_facebook = link_facebook
                insert_kontak.no_pengaduan = no_pengaduan
                insert_kontak.alamat = alamat
                insert_kontak.email_pengaduan = email_pengaduan
                insert_kontak.email_cs = email_cs
                insert_kontak.created_at = timezone.now()
                insert_kontak.save()

                messages.success(request, f"data berhasil Ditambahkan")
                return redirect('admin_setori:admin_kontak')
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal menambahkan")
            return redirect('admin_setori:admin_kontak')
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
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password


@method_decorator(login_required(), name='dispatch')
class ProfilViews(View):
    def get(self, request):
        dt_akun = Account.objects.all()
        akun={
            'dt_akun':dt_akun,
            'role':ROLE_CHOICES
        }
       
        return render(request, 'admin/profil/index.html',akun)
    

class Edit_profil(View):
    def post(self, request):

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        no_hp = request.POST.get('phone')
        id_user = request.POST.get('user_id')
        profil = request.FILES.get('foto_profil')
        print(profil)
        
        try:
            with transaction.atomic():
                insert_user = get_object_or_404(Account,id=id_user)
                insert_user.email = email
                insert_user.first_name = first_name
                insert_user.last_name = last_name
                insert_user.phone = no_hp
                insert_user.avatar = profil
                insert_user.save()
                messages.success(request, "berhasil edit profil!")
                return redirect('admin_setori:profil')  # Redirect to the list view
        except Exception as e:
            print('gagal mengedit profile', e)
            messages.error(request, "gagal mengedit profile ")
            return redirect('admin_setori:profil')
        

class Edit_password(View):
    def post(self, request):

        password_lama = request.POST.get('password_lama')

        password_baru = request.POST.get('password_baru')
        password_konfirmasi = request.POST.get('password_konfirmasi')
        id_user = request.POST.get('user_id')
        user = request.user

        # Verifikasi password lama
        if not check_password(password_lama, user.password):
            messages.error(request, "Password lama tidak cocok.")
            return redirect('admin_setori:profil')
        
        # Validasi password baru dan konfirmasi password
        if password_baru != password_konfirmasi:
            messages.error(request, "Password baru dan konfirmasi password tidak sama.")
            return redirect('admin_setori:profil')
        
        
       
        
        
        try:
            with transaction.atomic():
                user.set_password(password_baru)
                user.save()
                print('sukses edit password')
                
                # Pastikan sesi pengguna tetap aktif setelah password berubah
                update_session_auth_hash(request, user)
                messages.success(request, "Password berhasil diperbarui.")
                return redirect('admin_setori:profil')  # Ubah ke URL yang sesuai untuk halaman profil atau dashboard
            
        except Exception as e:
            print('gagal mengedit profile', e)
            messages.error(request, "gagal mengedit profile ")
            return redirect('admin_setori:profil')
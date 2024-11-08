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
class Master_jenis_kesehatanView(View):
    def get(self, request):
        dt_kesehatan = Jenis_kesehatan.objects.filter(deleted_at__isnull = True)

        data = {
            'dt_kesehatan': dt_kesehatan
        }

        return render(request, 'admin/master_jenis_kesehatan/index.html',data)
    
class Add_jenis_kesehatan(View):
     def post(self, request):
        
        jenis= request.POST.get('jenis_kesehatan')  # Fetch the name field from POST request
        try:
            with transaction.atomic():
                insert_jenis_kesehatan = Jenis_kesehatan()
                insert_jenis_kesehatan.nama_jenis = jenis
                insert_jenis_kesehatan.save()  # Save new category in the database

                messages.success(request, "data Jenis kesehatan berhasil ditambahakan")
                return redirect('admin_setori:master_jenis_kesehatan')  # Redirect to the list view
                
        except Exception as e:
            print('gagal menambahkan', e)
            messages.error(request, "gagal menambahkan")
            return redirect('admin_setori:master_jenis_kesehatan')
        
class Add_jenis_kesehatan(View):
     def post(self, request):
        
        jenis= request.POST.get('jenis_kesehatan')  # Fetch the name field from POST request
        try:
            with transaction.atomic():
                insert_jenis_kesehatan = Jenis_kesehatan()
                insert_jenis_kesehatan.nama_jenis = jenis
                insert_jenis_kesehatan.save()  # Save new category in the database

                messages.success(request, "data Jenis kesehatan berhasil tambahkan")
                return redirect('admin_setori:master_jenis_kesehatan')  # Redirect to the list view
                
        except Exception as e:
            print('gagal menambahkan', e)
            messages.error(request, "gagal menambahkan")
            return redirect('admin_setori:master_jenis_kesehatan')
        
class Edit_jenis_kesehatan(View):
     def post(self, request):
        
        jenis= request.POST.get('jenis_kesehatan')  # Fetch the name field from POST request
        try:
            with transaction.atomic():
                insert_jenis_kesehatan = Jenis_kesehatan()
                insert_jenis_kesehatan.nama_jenis = jenis
                insert_jenis_kesehatan.save()  # Save new category in the database

                messages.success(request, "data Jenis kesehatan berhasil diedit")
                return redirect('admin_setori:master_jenis_kesehatan')  # Redirect to the list view
                
        except Exception as e:
            print('gagal menambahkan', e)
            messages.error(request, "gagal menambahkan")
            return redirect('admin_setori:master_jenis_kesehatan')
        
class Deletejenis_kesehatan(View):
    def get(self, request, jenis_kesehatan_id):
        del_jenis_kesehatan = get_object_or_404(Jenis_kesehatan, jenis_kesehatan_id=jenis_kesehatan_id) 
        del_jenis_kesehatan.delete()  
        messages.success(request, "berhasil dihapus")
        return redirect('admin_setori:master_jenis_kesehatan')


    
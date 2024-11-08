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
class Master_indikator(View):
    def get(self, request,jenis_kesehatan_id):
        dt_kesehatan = Master_jenis_kesehatan.objects.filter(deleted_at__isnull = True,jenis_kesehatan_id=jenis_kesehatan_id)
        dt_indikator = Indikator_kesehatan.objects.filter(deleted_at__isnull = True,jenis_kesehatan_id=jenis_kesehatan_id)

        data = {
            'dt_indikator': dt_indikator,
            'dt_kesehatan': dt_kesehatan,

        }
        

        return render(request, 'admin/master_indikator/index.html',data)

class Add_indikator(View):
     def post(self, request):
        
        nama_indikator = request.POST.get("nama_indikator")
        jenis_kesehatan_id = request.POST.get("jenis_kesehatan")
        
        try:
            with transaction.atomic():
                
                insert_indikator = Indikator_kesehatan()
                insert_indikator.jenis_kesehatan =  Master_jenis_kesehatan.objects.get(jenis_kesehatan_id=jenis_kesehatan_id)
                insert_indikator.nama_indikator = nama_indikator
                insert_indikator.save()
             

                messages.success(request, "Indikator kesehatan berhasil ditambahkan.")
                return redirect(reverse('admin_setori:master_indikator',args=[jenis_kesehatan_id]))    
        except Exception as e:
            print('gagal menambahkan', e)
            messages.error(request, "gagal menambahkan")
            return redirect(reverse('admin_setori:master_indikator',args=[jenis_kesehatan_id])) 
        




 
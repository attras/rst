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
class Master_sliderViews(View):
    
    def get(self, request):
        
        breadcrump = [{
        'nama': 'Master slider',
        'url': reverse('admin_setori:master_slider'),
        }
        ]
        dt_slider = Slider.objects.filter(deleted_at__isnull = True)
        data ={
            'dt_slider':dt_slider,
            'breadcrump':breadcrump,
            'title': 'Master Slider',
        }
       
        return render(request, 'admin/master_slider/index.html',data)
    
class Add_slider(View):
    def get(self, request):
        dt_slider = Slider.objects.filter(deleted_at__isnull = True)
        data ={
            'dt_slider':dt_slider,
        }
       
        return render(request, 'admin/master_slider/form.html',data)
    
    def post(self, request):
        logo = request.FILES.get('logo')
        foto = request.FILES.get('foto')
        text = request.POST.get('text')
        status = request.POST.get('status')

        try :
            with transaction.atomic():
                insert_slider = Slider()
                insert_slider.logo = logo
                insert_slider.foto = foto
                insert_slider.text = text
                insert_slider.status = status
                insert_slider.save()
                messages.success(request, " added successfully!")
                return redirect('admin_setori:master_slider') 

        except Exception as e:
            print('Error while adding category', e)
            messages.error(request, "Failed to add ")
            return redirect('admin_setori:master_slider')

class Editslider(View):
    def get(self,request,id_slider):
        dt_slider = get_object_or_404(Slider,id_slider=id_slider,deleted_at__isnull = True)
        breadcrump = [{
        'nama': 'Master slider',
        'url': reverse('admin_setori:master_slider'),
        },
        {
        'nama': 'Edit Slider',
        'url': reverse('admin_setori:edit_slider',args=[id_slider]),
        },
        ]
        data ={
            'edit':True,
            'dt_slider':dt_slider,
            'id_slider' : id_slider,
            'breadcrump' : breadcrump,
            'title': 'Edit Slider',
        }
       
        return render(request, 'admin/master_slider/form.html',data)
     
    def post(self, request, id_slider):
        dt_slider = get_object_or_404(Slider, id_slider=id_slider, deleted_at__isnull=True)

        logo = request.FILES.get('logo') or dt_slider.logo
        foto = request.FILES.get('foto') or dt_slider.foto
        text = request.POST.get('text')
        status = request.POST.get('status')
        try:
            with transaction.atomic():
                
                insert_slider = get_object_or_404(Slider,id_slider=id_slider)
                insert_slider.logo = logo
                insert_slider.foto = foto
                insert_slider.text = text
                insert_slider.status = status
                insert_slider.updated_at = timezone.now()
                insert_slider.save()  # Save new category in the database

                messages.success(request, "Category edit successfully!")
                return redirect('admin_setori:edit_slider',id_slider)  # Redirect to the list view
                
        except Exception as e:
            print('Error while editing category', e)
            messages.error(request, "Failed to edit category")
            return redirect(reverse('admin_setori:master_slider'))

class Delete_slider(View):
    def get(self, request, id_slider):
        del_slider = get_object_or_404(Slider,id_slider=id_slider)
        del_slider.delete()
        messages.success(request, f"data berhasil dihapus")
        return redirect('admin_setori:master_slider')

class Delete_at_slider(View):
    def get(self, request, id_slider):
        try:
            with transaction.atomic():
                del_slider = get_object_or_404(Slider,id_slider=id_slider)
                del_slider.deleted_at = timezone.now()
                del_slider.save()
                messages.success(request, f"data berhasil dihapus")
                return redirect('admin_setori:master_slider')
                
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal menghapus")
            return redirect('admin_setori:master_slider')


class Historislider(View):
    def get(self, request):
        dt_slider = Slider.objects.filter(deleted_at__isnull = False)
        breadcrump = [{
        'nama': 'Master slider',
        'url': reverse('admin_setori:master_slider'),
        },
        {
        'nama': 'Riwayat Slider',
        'url': reverse('admin_setori:histori_slider'),
        },
        ]
        data ={
            'dt_slider':dt_slider,
            'breadcrump':breadcrump,
            'title':'Riwayat Hapus Master Slider'
        }
       
        return render(request, 'admin/master_slider/histori.html',data)
    
class Restoreslider(View):
    def get(self, request, id_slider):
        try:
            with transaction.atomic():
                del_layanan = get_object_or_404(Slider,id_slider=id_slider)
                del_layanan.deleted_at = None
                del_layanan.save()
                messages.success(request, f"data berhasil dipulihkan")
                return redirect('admin_setori:histori_slider')
                
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal menghapus")
            return redirect('admin_setori:histori_slider')
             





    

           


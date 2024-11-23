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
        dt_slider = Slider.objects.filter(deleted_at__isnull = True)
        data ={
            'dt_slider':dt_slider,
        }
       
        return render(request, 'admin/master_slider/index.html',data)
    
class Add_slider(View):
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
    def post(self, request, id_slider):
        logo = request.FILES.get('logo')
        foto = request.FILES.get('foto')
        text = request.POST.get('text')
        status = request.POST.get('status')
        try:
            with transaction.atomic():
                
                insert_category = get_object_or_404(Slider,id_slider=id_slider)
                insert_slider.logo = logo
                insert_slider.foto = foto
                insert_slider.text = text
                insert_slider.status = status
                insert_category.updated_at = timezone.now()
                insert_category.save()  # Save new category in the database

                messages.success(request, "Category edit successfully!")
                return redirect('admin_setori:master_slider')  # Redirect to the list view
                
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
        data ={
            'dt_slider':dt_slider,
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
             





    

           


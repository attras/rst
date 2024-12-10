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
from admin_setori.decorators import role_required, admin_only
from django.utils.decorators import method_decorator

@method_decorator(login_required(), name='dispatch')
# @method_decorator(admin_only(), name='dispatch')
class Master_kategoriViews(View):
    def get(self, request):
        breadcrump = [{
        'nama': 'Master Jenis Kesehatan',
        'url': reverse('admin_setori:master_jenis_kesehatan'),
        }
        ]
        dt_category = Master_sarpras.objects.all()
        data = {
            'dt_category': dt_category,
            'breadcrump':breadcrump,
            'title':'Master sarpras'
        }
        return render(request, 'admin/master_sarpras/index.html',data)

class AddSarpras(View):
    def post(self, request):
        sarpras_name = request.POST.get('name')  # Fetch the name field from POST request
        try:
            with transaction.atomic():
                insert_sarpras = Master_sarpras()
                insert_sarpras.nama = sarpras_name
                insert_sarpras.save()  # Save new category in the database

                messages.success(request, "Category added successfully!")
                return redirect('admin_setori:master_sarpras')  # Redirect to the list view
                
        except Exception as e:
            print('Error while adding category', e)
            messages.error(request, "Failed to add category")
            return redirect('admin_setori:master_sarpras')

    
class EditSarpras(View):
    def post(self, request, id):
        name = request.POST.get('name')  # Fetch the name field from POST request
        try:
            with transaction.atomic():
                
                insert_sarpras = get_object_or_404(Master_sarpras,id=id)
                insert_sarpras.nama = name
                insert_sarpras.updated_at = timezone.now()
                insert_sarpras.save()  # Save new category in the database

                messages.success(request, "Category edit successfully!")
                return redirect('admin_setori:master_sarpras')  # Redirect to the list view
                
        except Exception as e:
            print('Error while editing category', e)
            messages.error(request, "Failed to edit category")
            return redirect(reverse('admin_setori:master_sarpras'))
        


# Delete a Category (DeleteCategory)
class DeleteSarpras(View):
    def get(self, request, id):
        del_sarpras = get_object_or_404(Master_sarpras, id=id)  # Fetch category by UUID
        del_sarpras.delete()  # Delete the category
        messages.success(request, "Category deleted successfully!")
        return redirect('admin_setori:master_sarpras')


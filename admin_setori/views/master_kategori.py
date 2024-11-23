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
        dt_category = Category.objects.filter(deleted_at__isnull = True)
        data = {
            'dt_category': dt_category
        }
        return render(request, 'admin/master_kategori/index.html',data)

class AddCategory(View):
    def post(self, request):
        category_name = request.POST.get('name')  # Fetch the name field from POST request
        try:
            with transaction.atomic():
                insert_category = Category()
                insert_category.name = category_name
                insert_category.save()  # Save new category in the database

                messages.success(request, "Category added successfully!")
                return redirect('admin_setori:master_kategori')  # Redirect to the list view
                
        except Exception as e:
            print('Error while adding category', e)
            messages.error(request, "Failed to add category")
            return redirect('admin_setori:master_kategori')

    
class EditCategory(View):
    def post(self, request, categori_id):
        name = request.POST.get('name')  # Fetch the name field from POST request
        try:
            with transaction.atomic():
                
                insert_category = get_object_or_404(Category,categori_id=categori_id)
                insert_category.name = name
                insert_category.updated_at = timezone.now()
                insert_category.save()  # Save new category in the database

                messages.success(request, "Category edit successfully!")
                return redirect('admin_setori:master_kategori')  # Redirect to the list view
                
        except Exception as e:
            print('Error while editing category', e)
            messages.error(request, "Failed to edit category")
            return redirect(reverse('admin_setori:master_kategori'))
        


# Delete a Category (DeleteCategory)
class DeleteCategory(View):
    def get(self, request, categori_id):
        del_category = get_object_or_404(Category, categori_id=categori_id)  # Fetch category by UUID
        del_category.delete()  # Delete the category
        messages.success(request, "Category deleted successfully!")
        return redirect('admin_setori:master_kategori')


class Delete_at_kategori(View):
    def get(self, request, categori_id):
        try:
            with transaction.atomic():
                del_category = get_object_or_404(Category,categori_id=categori_id)
                del_category.deleted_at = timezone.now()
                del_category.save()
                messages.success(request, f"data berhasil dihapus")
                return redirect('admin_setori:master_kategori')
                
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal menghapus")
            return redirect('admin_setori:master_kategori')


class Historikategori(View):
    def get(self, request):
        dt_category = Category.objects.filter(deleted_at__isnull = False)
        data = {
            'dt_category': dt_category
        }
        return render(request, 'admin/master_kategori/histori.html',data)
    
class Restorekategori(View):
    def get(self, request, categori_id):
        try:
            with transaction.atomic():
                del_layanan = get_object_or_404(Category,categori_id=categori_id)
                del_layanan.deleted_at = None
                del_layanan.save()
                messages.success(request, f"data berhasil dipulihkan")
                return redirect('admin_setori:histori_kategori')
                
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal menghapus")
            return redirect('admin_setori:histori_kategori')

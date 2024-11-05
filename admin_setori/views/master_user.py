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
class Master_userViews(View):
    def get(self, request):
        dt_akun = Account.objects.all()
        akun={
            'dt_akun':dt_akun,
            'role':ROLE_CHOICES
        }
       
        return render(request, 'admin/master_user/index.html',akun)
    
class AddUser(View):
    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        try:
            with transaction.atomic():
                insert_user = Account()
                insert_user.email = email
                insert_user.username = username
                insert_user.phone = phone
                insert_user.password = password
                insert_user.role = role
                insert_user.set_password(password)
                insert_user.save()
                messages.success(request, " added successfully!")
                return redirect('admin_setori:master_user')  # Redirect to the list view
        except Exception as e:
            print('Error while adding category', e)
            messages.error(request, "Failed to add ")
            return redirect('admin_setori:master_user')
        

class DeleteUser(View):
    def get(self, request, id):
        del_user = get_object_or_404(Account,id=id)
        del_user.delete()
        messages.success(request, f"data berhasil dihapus")
        return redirect('admin_setori:master_user')

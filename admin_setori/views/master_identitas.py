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
class Master_identitasViews(View):
    def get(self, request):
        dt_identitas = MasterIdentitass.objects.all()
        data = {
            'dt_identitas': dt_identitas
        }

        return render(request, 'admin/master_identitas/index.html',data)
    
class AddIdentitas(View):
    def post(self, request):
        identitas = request.POST.get('identitas')
        try:
            with transaction.atomic():
                insert_identitas = MasterIdentitass()
                insert_identitas.identitas = identitas
                insert_identitas.save()

                messages.success(request, "Identitas berhasil ditambahkan.")
                return redirect('admin_setori:master_identitas')
        except Exception as e:
            print('Error Data', e)
            messages.error(request, "Gagal menambahkan identitas.")
            return redirect('admin_setori:master_identitas')

class DeleteIdentitas(View):
    def get(self, request, id_identitas):
        del_identitas = get_object_or_404(MasterIdentitass, id=id_identitas)
        del_identitas.delete()
        messages.success(request, "Identitas berhasil dihapus.")
        return redirect('admin_setori:master_identitas')
    
class EditIdentitas(View):
    def get(self, request, identitas_id):
        # Ambil data identitas berdasarkan UUID
        identitas = get_object_or_404(MasterIdentitass, id=identitas_id)
        return render(request, 'edit_identitas.html', {'identitas': identitas})

    def post(self, request, identitas_id):
        # Ambil data identitas berdasarkan UUID
        identitas = get_object_or_404(MasterIdentitass, id=identitas_id)
        
        # Ambil data yang dikirim melalui POST
        new_identitas = request.POST.get('identitas')

        try:
            # Update data identitas
            identitas.identitas = new_identitas
            identitas.save()

            messages.success(request, "Identitas updated successfully!")
            return redirect('admin_setori:identitas_list')  # Redirect ke list identitas
        except Exception as e:
            print("Error while updating identitas", e)
            messages.error(request, "Failed to update identitas")
            return render(request, 'edit_identitas.html', {'identitas': identitas})
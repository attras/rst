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



class Admin_faqViews(View):
    def get(self, request):
        dt_faq = Faq.objects.filter(deleted_at__isnull = True)
        data = {
            'dt_faq' : dt_faq
        }
        return render(request, 'admin/admin_faq/index.html',data)

class Addfaq(View) :
    def post(self, request):
        pertanyaan = request.POST.get('pertanyaan')
        jawaban = request.POST.get('jawaban')
        try:
            with transaction.atomic():
                insert_faq = Faq()
                insert_faq.pertanyaan = pertanyaan
                insert_faq.jawaban = jawaban
                insert_faq.created_at = timezone.now()
                insert_faq.save()

                messages.success(request, f"data berhasil Ditambahkan")
                return redirect('admin_setori:admin_faq')
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal menambahkan")
            return redirect('admin_setori:admin_faq')
        


class Editfaq(View) :
    def post(self, request,id_faq):
        pertanyaan = request.POST.get('pertanyaan')
        jawaban = request.POST.get('jawaban')
        try:
            with transaction.atomic():
                insert_faq = get_object_or_404(Faq, faq_id=id_faq)
                insert_faq.pertanyaan = pertanyaan
                insert_faq.jawaban = jawaban
                insert_faq.created_at = timezone.now()
                insert_faq.save()

                messages.success(request, f"data berhasil diedit")
                return redirect('admin_setori:admin_faq')
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal edit")
            return redirect(reverse('admin_setori:admin_faq'))



class DeleteAt(View):
    def get(self, request, id_faq):
        try:
            with transaction.atomic():
                del_faq = get_object_or_404(Faq,faq_id=id_faq)
                del_faq.deleted_at = timezone.now()
                del_faq.save()
                messages.success(request, f"data berhasil dihapus")
                return redirect('admin_setori:admin_faq')
                
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal menghapus")
            return redirect('admin_setori:admin_faq')
    
class Historifaq(View):
    def get(self, request):
        dt_faq = Faq.objects.filter(deleted_at__isnull = False)
        data = {
            'dt_faq' : dt_faq
        }
        return render(request, 'admin/admin_faq/histori.html',data)
    
class Restorefaq(View):
    def get(self, request, id_faq):
        try:
            with transaction.atomic():
                del_faq = get_object_or_404(Faq,faq_id=id_faq)
                del_faq.deleted_at = None
                del_faq.save()
                messages.success(request, f"data berhasil dipulihkan")
                return redirect('admin_setori:histori_faq')
                
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal menghapus")
            return redirect('admin_setori:histori_faq')
    
    
    

class Deletefaq(View):
    def get(self, request, faq_id):
        try:
            with transaction.atomic():
                del_faq = get_object_or_404(Faq,faq_id=faq_id)
                del_faq.delete()
                messages.success(request, f"data berhasil dihapus")
                return redirect('admin_setori:histori_faq')
        except Exception as e:
            print('Error Data', e)
            messages.error(request,"gagal menghapus")
            return redirect('admin_setori:histori_faq')

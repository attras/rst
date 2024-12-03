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
class Admin_beritaViews(View):
    def get(self, request):
        breadcrump = [{
        'nama': 'Berita',
        'url': reverse('admin_setori:admin_berita'),
        }
        ]
        dt_berita = News.objects.filter(deleted_at__isnull = True)
        dt_kategori = Category.objects.filter(deleted_at__isnull = True)
        data = {
            'dt_berita' : dt_berita,
            'dt_kategori' : dt_kategori,
            'breadcrump' : breadcrump,
            'title' : 'Berita'

        }
        return render(request, 'admin/admin_berita/berita.html',data)
class Detail_Berita(View):
    def get(self, request, slug):
        detail_berita = get_object_or_404(News,slug=slug)
        dt_berita = News.objects.filter(deleted_at__isnull=True).order_by('-created_at')  # Ambil semua berita yang tidak dihapus
        dt_category = Category.objects.filter(deleted_at__isnull = True)  # Ambil semua kategori yang tidak dihapus

        data = {
            'dt_berita': dt_berita,
            'detail_berita': detail_berita,
            'dt_category': dt_category,
        }
        return render(request, 'admin/admin_berita/detail.html', data)
    
class AddBerita(View):
    def get(self, request):
        dt_berita = News.objects.filter(deleted_at__isnull = True)
        dt_kategori = Category.objects.filter(deleted_at__isnull = True)
        data = {
            'dt_berita' : dt_berita,
            'dt_kategori' : dt_kategori

        }
        return render(request, 'admin/admin_berita/form.html',data)
    def post(self, request):
        title = request.POST.get('title')
        content = request.POST.get('content_berita')
        category_id = request.POST.get('category')  # Get the selected category ID
        thumbnail = request.FILES.get('thumbnail')
        username = request.POST.get('username')  # Assuming the username is passed in the request

        try:
            with transaction.atomic():
                # Find the selected category by its UUID
                selected_category = Category.objects.get(categori_id=category_id)
                
                # Find the Account by username
                created_by = Account.objects.get(username=username)

                # Create new News object
                insert_news = News()
                insert_news.title = title
                insert_news.content = content
                insert_news.thumbnail = thumbnail
                insert_news.slug = generate_unique_slug(insert_news)
                insert_news.category = selected_category  # Set the category by the selected object
                insert_news.created_by = created_by  # Set the created_by field based on the username
                insert_news.last_updated_by = None
                insert_news.seen = 0
                insert_news.jenis = request.POST.get('jenis')
                insert_news.created_at =  timezone.now()

                # Save the News object
                insert_news.save()

                # Display success message and redirect
                messages.success(request, f"News '{title}' has been successfully added by {created_by.username}.")
                return redirect('admin_setori:admin_berita')
        
        except Account.DoesNotExist:
            messages.error(request, "The username provided does not exist.")
            return redirect('admin_setori:admin_berita')

        except Category.DoesNotExist:
            messages.error(request, "Selected category does not exist.")
            return redirect('admin_setori:admin_berita')
        
        except Exception as e:
            print('Error adding News:', e)
            messages.error(request, "Failed to add news. Please try again.")
            return redirect('admin_setori:admin_berita')
        
class Editberita(View):
    def get(self, request,id):
        dt_berita = get_object_or_404(News,id=id)
        dt_kategori = Category.objects.filter(deleted_at__isnull = True)
        data = {
            'dt_berita' : dt_berita,
            'dt_kategori' : dt_kategori,
            'edit': True
            

        }
        return render(request, 'admin/admin_berita/form.html',data)
    
    def post(self, request,id):
        dt_berita = get_object_or_404(News,id=id)
        title = request.POST.get('title')
        content = request.POST.get('content_berita')
        category_id = request.POST.get('category')  # Get the selected category ID
        thumbnail = request.FILES.get('thumbnail') or dt_berita.thumbnail
        username = request.POST.get('username')  # Assuming the username is passed in the request

        try:
            with transaction.atomic():
                # Find the selected category by its UUID
                selected_category = Category.objects.get(categori_id=category_id)
                
                # Find the Account by username
                created_by = Account.objects.get(username=username)

                # Create new News object
                insert_news = get_object_or_404(News,id=id)
                insert_news.title = title
                insert_news.content = content
                insert_news.thumbnail = thumbnail
                insert_news.slug = generate_unique_slug(insert_news)
                insert_news.category = selected_category  # Set the category by the selected object
                insert_news.last_updated_by = username
                insert_news.updated_at =  timezone.now()

                # Save the News object
                insert_news.save()

                # Display success message and redirect
                messages.success(request, f"News '{title}' has been successfully added by {created_by.username}.")
                return redirect('admin_setori:admin_berita')
        
        except Account.DoesNotExist:
            messages.error(request, "The username provided does not exist.")
            return redirect('admin_setori:admin_berita')

        except Category.DoesNotExist:
            messages.error(request, "Selected category does not exist.")
            return redirect('admin_setori:admin_berita')
        
        except Exception as e:
            print('Error adding News:', e)
            messages.error(request, "gagal edit")
            return redirect('admin_setori:admin_berita')

class Deleteberita(View):
    def get(self, request, news_slug):
        del_news = get_object_or_404(News, slug=news_slug)
        del_news.delete()
        messages.success(request, "Data berhasil dihapus")
        return redirect('admin_setori:admin_berita')



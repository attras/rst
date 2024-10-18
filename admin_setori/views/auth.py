from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views import View 
from django.contrib import messages
from admin_setori.models import *
import re
from django.utils.decorators import method_decorator
from django.urls import reverse

def check_is_email(email):

    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return bool(re.match(email_regex,email))

class LoginViews(View):
    def get(self, request):
        data = {
            'page_title': 'login',
            # 'breadcumb': [{'title': 'SIMDIKOAP', 'url':reverse('app:index_admin')}],
        }
        return render(request, 'admin/login.html', data)

    def post(self, request):
        if not request.user.is_authenticated:
            email = request.POST.get('email')
            pwd = request.POST.get('pwd')
            print(f"Email: {email}")
            print(f"Password: {pwd}")
            is_email = check_is_email(email)
            
            if is_email:
                user = authenticate(request, email=email, password=pwd)
            else:
                try:
                    user = Account.objects.get(username = email, is_active = True)
                    if not user.check_password(pwd):
                        user = None
                except Exception as e:
                    user = None
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Selamat datang {user.username} ({user.get_role_display().upper()})")
                print('masuk')
                if request.GET.get('next') is not None:
                    return redirect(request.GET.get('next'))
                else:
                    # messages.success(request, f"Selamat datang {user.username} ({user.get_role_display().upper()})")
                    # print(f"cekkk")
                    return redirect('admin_setori:dashboard')
            else:
                messages.error(request, "Login gagal, silahkan masukkan data dengan benar")
                print(f"Login gagal ")
                return redirect('admin_setori:halaman_login')
        else:
            print(f"Login berhasil ")
            return redirect('admin_setori:dashboard')
            


@method_decorator(login_required(), name='dispatch')
class LogoutViews(View):
    def get(self, request):
        logout_message = request.GET.get('logout_message', None)
        if logout_message is not None:
            messages.info(request, logout_message)
        logout(request)
        return redirect('admin_setori:halaman_login')


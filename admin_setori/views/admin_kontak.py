from django.shortcuts import render, redirect
from django.db import transaction 
from django.views import View
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
# from admin_setori.models import Contact

class Admin_kontakViews(View):
    def get(self, request):
        
        return render(request, 'admin/admin_kontak/index.html')
    

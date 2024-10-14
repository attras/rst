from django.shortcuts import render, redirect

from django.views import View
from admin_setori.models import *

class Master_userViews(View):
    def get(self, request):
       
        return render(request, 'admin/master_user/master_user.html')
    

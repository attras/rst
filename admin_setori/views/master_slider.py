from django.shortcuts import render, redirect
from django.db import transaction 
from django.views import View
from django.contrib import messages
from admin_setori.models import *

class Master_sliderViews(View):
    def get(self, request):
        return render(request, 'admin/master_slider/index.html')
    

           


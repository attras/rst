from django.shortcuts import render, redirect
from django.db import transaction 
from django.views import View
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from admin_setori.models import *
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.text import slugify

class Master_identitasViews(View):
    def get(self, request):
      

        return render(request, 'admin/master_identitas/index.html')
    

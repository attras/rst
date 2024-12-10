from django.shortcuts import render, redirect

from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required(), name='dispatch')
class Admin_indexViews(View):
    def get(self, request):
        breadcrump = [{
        'nama': 'Dashboard',
        'url': '',
        }]
        data = {
           
            'breadcrump': breadcrump,
            'title':'Dashboard'

            
        }

        return render(request, 'admin/admin_dashboard/index.html',data)
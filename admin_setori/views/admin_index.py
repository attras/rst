from django.shortcuts import render, redirect

from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required(), name='dispatch')
class Admin_indexViews(View):
    def get(self, request):

        return render(request, 'admin/admin_dashboard/index.html')
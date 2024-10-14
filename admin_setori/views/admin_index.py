from django.shortcuts import render, redirect

from django.views import View


class Admin_indexViews(View):
    def get(self, request):
        return render(request, 'admin/base_layout/index.html')
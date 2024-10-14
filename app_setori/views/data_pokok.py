from django.shortcuts import render, redirect

from django.views import View


class Data_pokokViews(View):
    def get(self, request):
        
        return render(request, 'setori/data_pokok/index.html')
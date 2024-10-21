from django.shortcuts import render, redirect

from django.views import View


class Data_pokokViews(View):
    def get(self, request):
        
        return render(request, 'setori/data_pokok/index.html')

class DetaildataViews(View):
    def get(self, request):
        return render(request, 'setori/data_pokok/data_rinci.html')
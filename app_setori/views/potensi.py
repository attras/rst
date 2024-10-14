from django.shortcuts import render, redirect

from django.views import View


class PotensiViews(View):
    def get(self, request):
        return render(request, 'setori/potensidaerah/index.html')

class DetailpotensiViews(View):
    def get(self, request):
        return render(request, 'setori/potensidaerah/detailkampung.html')
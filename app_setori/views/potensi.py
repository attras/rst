from django.shortcuts import render, redirect

from django.views import View


class PotensiViews(View):
    def get(self, request):
        return render(request, 'setori/potensidaerah/index.html')

class DistrikpotensiViews(View):
    def get(self, request):
        return render(request, 'setori/potensidaerah/distrik_lengkap.html')

class DetailpotensidistrikViews(View):
    def get(self, request):
        return render(request, 'setori/potensidaerah/detaildistrik.html')

class DetailpotensikampungViews(View):
    def get(self, request):
        return render(request, 'setori/potensidaerah/detailkampung.html')
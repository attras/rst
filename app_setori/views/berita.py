from django.shortcuts import render, redirect

from django.views import View


class BeritaViews(View):
    def get(self, request):
        return render(request, 'setori/berita/index.html')

class DetailberitaViews(View):
    def get(self, request):
        return render(request, 'setori/detail_berita/index.html')
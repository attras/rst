from django.shortcuts import render, redirect

from django.views import View


class LayananViews(View):
    def get(self, request):
        return render(request, 'setori/layanan/index.html')
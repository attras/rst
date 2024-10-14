from django.shortcuts import render, redirect

from django.views import View


class KontakViews(View):
    def get(self, request):
        return render(request, 'setori/kontak/index.html')
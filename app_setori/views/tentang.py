from django.shortcuts import render, redirect

from django.views import View


class TentangViews(View):
    def get(self, request):
        return render(request, 'setori/tentang_kami/index.html')
from django.urls import path,include,re_path
# from django.conf.urls import url,handler403

from .views import *
from .views import beranda
from .views import berita
from .views import data_pokok
from .views import faq
from .views import kontak
from .views import layanan
from .views import potensi
from .views import tentang

app_name = 'app_setori'

urlpatterns = [
     path('', beranda.HomeViews.as_view(), name = 'index_home'),
     path('berita', berita.BeritaViews.as_view(), name = 'berita'),
     path('data', data_pokok.Data_pokokViews.as_view(), name = 'data'),
     path('detail_data', data_pokok.DetaildataViews.as_view(), name = 'detail_data'),
     path('potensi', potensi.PotensiViews.as_view(), name = 'potensi'),
     path('detail_potensi', potensi.DetailpotensikampungViews.as_view(), name = 'detail_potensi'),
     path('distrik', potensi.DistrikpotensiViews.as_view(), name = 'distrik'),
     path('detail_distrik', potensi.DetailpotensidistrikViews.as_view(), name = 'detail_distrik'),
     path('layanan', layanan.LayananViews.as_view(), name = 'layanan'),
     path('faq', faq.FaqViews.as_view(), name = 'faq'),
     path('tentang', tentang.TentangViews.as_view(), name = 'tentang'),
     path('kontak', kontak.KontakViews.as_view(), name = 'kontak'),
     path('detail_berita', berita.DetailberitaViews.as_view(), name = 'detail_berita'),
]
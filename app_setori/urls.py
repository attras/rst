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
     path('data', data_pokok.Data_pokokViews.as_view(), name = 'data'),
     path('api/tenaga-kesehatan-data/', data_pokok.TenagaKesehatanDataViews.as_view(), name='tenaga-kesehatan-data'),
     path('detail_data', data_pokok.DetaildataViews.as_view(), name = 'detail_data'),
     
     path('layanan', layanan.LayananViews.as_view(), name = 'layanan'),
     path('faq', faq.FaqViews.as_view(), name = 'faq'),
     path('tentang', tentang.TentangViews.as_view(), name = 'tentang'),
     path('kontak', kontak.KontakViews.as_view(), name = 'kontak'),

     path('berita/',include([
     path('', berita.BeritaViews.as_view(), name = 'berita'),
     path('detail/<slug:slug>/', berita.DetailberitaViews.as_view(), name='detail_berita'),
     ])),

     path('potensi/',include([
          path('kampung', potensi.PotensiViews.as_view(), name = 'kampung'),
          path('distrik', potensi.PotensiDistrikViews.as_view(), name = 'distrik'),
          path('detail/<str:info_wilayah_id>', potensi.DistridetailViews.as_view(), name = 'detail'),
     ])),
     
]
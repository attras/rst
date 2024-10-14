from django.urls import path,include,re_path
# from django.conf.urls import url,handler403

from .views import *

app_name = 'admin_setori'
urlpatterns = [
    # path('login', auth.LogViews.as_view(), name = 'login'),
    path('dashboard/',admin_index.Admin_indexViews.as_view(), name = 'dashboard'),
    path('master_user', master_user.Master_userViews.as_view(), name = 'master_user'),
   
    path('master_kategori', master_kategori.Master_kategoriViews.as_view(), name = 'master_kategori'),
    # path('add_kategori',master_kategori.Addkategori.as_view(),name='add_kategori'),

    path('faq/',include([
        path('',admin_faq.Admin_faqViews.as_view(),name='admin_faq'),
        path('add_faq',admin_faq.Addfaq.as_view(),name='add_faq'),
        # path('edit_faq/<str:id_faq>',admin_faq.Editfaq.as_view(),name='edit_faq'),
        path('hapus_faq/<str:id_faq>',admin_faq.Deletefaq.as_view(),name='hapus_faq'),
      
        ])),

    path('kontak/',include([
        path('',admin_kontak.Admin_kontakViews.as_view(),name='admin_kontak'),
        # path('add_kontak',admin_kontak.AddContact.as_view(),name='add_kotak'),
        ])),
    
    path('master_wilayah/',include([
        path('', master_wilayah.Master_wilayahViews.as_view(), name = 'master_wilayah'),
        # path('add', master_wilayah.AddMasterWilayah.as_view(), name = 'add_master_wilayah'),
        ])),
    
    path('master_identitas/',include([
        path('', master_identitas.Master_identitasViews.as_view(), name = 'master_identitas'),
        # path('add_master_identitas', master_identitas.AddMasterIdentitas.as_view(), name = 'add_master_identitas'),
        # path('edit/<slug:identitas_slug>/', master_identitas.EditMasterIdentitas.as_view(), name = 'edit_master_identitas'),
        # path('delete/<slug:identitas_slug>/', master_identitas.DeleteMasterIdentitas.as_view(), name = 'delete_master_identitas'),
        ])),

    path('master_slider/',master_slider.Master_sliderViews.as_view(),name='master_slider'),
    # path('add_slider',master_slider.Addslider.as_view(),name='add_slider'),
]
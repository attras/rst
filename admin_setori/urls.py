from django.urls import path,include,re_path
# from django.conf.urls import url,handler403

from .views import *

app_name = 'admin_setori'
urlpatterns = [
    path('', auth.LoginViews.as_view(), name = 'halaman_login'),
    path('logout', auth.LogoutViews.as_view(), name = 'logout_admin'),

    path('dashboard/',admin_index.Admin_indexViews.as_view(), name = 'dashboard'),
    
     path('master_user/',include([
         path('', master_user.Master_userViews.as_view(), name = 'master_user'),
         path('add', master_user.AddUser.as_view(), name = 'add_user'),
         path('delete/<int:id>', master_user.DeleteUser.as_view(), name = 'del_user'),
         ])),
         
    path('admin_berita/', include([
        path('', admin_berita.Admin_beritaViews.as_view(), name='admin_berita'),
        path('add', admin_berita.AddBerita.as_view(), name='add_berita'),
        path('delete/<slug:news_slug>/', admin_berita.Deleteberita.as_view(), name='delete_berita'),
    ])),

    path('kategori/',include([
        path('', master_kategori.Master_kategoriViews.as_view(), name = 'master_kategori'),
        path('add', master_kategori.AddCategory.as_view(), name = 'add_kategori'),
        path('edit/<str:categori_id>', master_kategori.EditCategory.as_view(), name = 'edit_kategori'),
        path('del/<str:category_id>', master_kategori.DeleteCategory.as_view(), name = 'del_kategori'),
        
        ])),
    
    # path('add_kategori',master_kategori.Addkategori.as_view(),name='add_kategori'),

    path('faq/',include([
        path('',admin_faq.Admin_faqViews.as_view(),name='admin_faq'),
        path('add_faq',admin_faq.Addfaq.as_view(),name='add_faq'),
        path('edit_faq/<str:id_faq>',admin_faq.Editfaq.as_view(),name='edit_faq'),
        path('delete_at/<str:id_faq>',admin_faq.DeleteAt.as_view(),name='delete_at_faq'),
        path('delete_faq/<str:faq_id>',admin_faq.Deletefaq.as_view(),name='delete_faq'),
        path('histori/',admin_faq.Historifaq.as_view(),name='histori_faq'),
        path('restore/<str:id_faq>',admin_faq.Restorefaq.as_view(),name='restore_faq'),
      
        ])),

    path('kontak/',include([
        path('',admin_kontak.Admin_kontakViews.as_view(),name='admin_kontak'),
        # path('add_kontak',admin_kontak.AddContact.as_view(),name='add_kotak'),
        ])),
    
    path('master_wilayah/',include([
        path('', master_wilayah.Master_wilayahViews.as_view(), name = 'master_wilayah'),
        path('add', master_wilayah.AddWilayah.as_view(), name = 'add_wilayah'),
        path('delete/<str:wilayah_id>', master_wilayah.DeleteWilayah.as_view(), name = 'delete_wilayah'),
       
        ])),
    
    path('master_identitas/',include([
        path('', master_identitas.Master_identitasViews.as_view(), name = 'master_identitas'),
        path('add_master_identitas', master_identitas.AddIdentitas.as_view(), name = 'add_identitas'),
        path('edit/<uuid:identitas_id>/', master_identitas.EditIdentitas.as_view(), name = 'edit_identitas'),
        path('delete/<uuid:id_identitas>', master_identitas.DeleteIdentitas.as_view(), name = 'delete_identitas'),
        ])),

    path('master_slider/',include([
        path('',master_slider.Master_sliderViews.as_view(),name='master_slider'),
        path('add_slider/',master_slider.Add_slider.as_view(),name='add_slider'),
        path('delete_slider/<uuid:id>',master_slider.Delete_slider.as_view(),name='delete_slider'),
        ])),

    path('admin_layanan/',include([
        path('',layanan.LayananViews.as_view(),name='admin_layanan'),
        path('add_layanan/',layanan.Addlayanan.as_view(),name='add_layanan'),
        path('edit_layanan/<str:id_layanan>/',layanan.Editlayanan.as_view(),name='edit_layanan'),
        path('delete_at/<str:id_layanan>/',layanan.Delete_at.as_view(),name='delete_at_layanan'),
        path('delete/<str:id_layanan>/',layanan.Deletelayanan.as_view(),name='delete_layanan'),
        path('histori/',layanan.Historilayanan.as_view(),name='histori_layanan'),
        path('restore/<str:id_layanan>/',layanan.Restorelayanan.as_view(),name='restore_layanan'),
        ])),

    # path('add_slider',master_slider.Addslider.as_view(),name='add_slider'),

    path('info_wilayah/',include([
        path('',admin_info_wilayah.Info_wilayahViews.as_view(),name='admin_info_wilayah'),
        path('add_info_wilayah',admin_info_wilayah.AddInfoWilayah.as_view(),name='add_info_wilayah'),
        ])),

    path('data_kesehatan/',include([
         path('',admin_data_kesehatan.Admin_data_kesehatanViews.as_view(),name='data_kesehatan'),
         
         ])),

    path('data_penduduk/',include([
         path('',admin_data_penduduk.Admin_data_pendudukViews.as_view(),name='data_penduduk'),
         path('add/',admin_data_penduduk.Add_data_penduduk.as_view(),name='add_data_penduduk'),
         
         ])),

    path('kontak/',include([
        path('',admin_kontak.Admin_kontakViews.as_view(),name='admin_kontak'),
        path('add_kontak/',admin_kontak.Addkontak.as_view(),name='add_kontak'),
        path('edit_kontak/<str:id>',admin_kontak.Editkontak.as_view(),name='edit_kontak'),
      
        ])),

]
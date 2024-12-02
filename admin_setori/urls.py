from django.urls import path,include,re_path
# from django.conf.urls import url,handler403

from .views import *

app_name = 'admin_setori'
urlpatterns = [
    path('', auth.LoginViews.as_view(), name = 'halaman_login'),
    path('logout', auth.LogoutViews.as_view(), name = 'logout_admin'),

    path('dashboard/',admin_index.Admin_indexViews.as_view(), name = 'dashboard'),
    path('profil/',include([
        path('',profil.ProfilViews.as_view(),name='profil'),
        path('edit/',profil.Edit_profil.as_view(),name='edit_profil'),
        path('edit_password/',profil.Edit_password.as_view(),name='edit_password'),
        ])),

    path('master_user/',include([
         path('', master_user.Master_userViews.as_view(), name = 'master_user'),
         path('add', master_user.AddUser.as_view(), name = 'add_user'),
         path('delete/<int:id>', master_user.DeleteUser.as_view(), name = 'del_user'),
         ])),
         
    path('admin_berita/', include([
        path('', admin_berita.Admin_beritaViews.as_view(), name='admin_berita'),
        path('add', admin_berita.AddBerita.as_view(), name='add_berita'),
        path('detail/<slug:slug>/', admin_berita.Detail_Berita.as_view(), name='detail_berita'),
        path('edit/<str:id>/', admin_berita.Editberita.as_view(), name='edit_berita'),
        
        path('delete/<slug:news_slug>/', admin_berita.Deleteberita.as_view(), name='delete_berita'),
    ])),

    path('kategori/',include([
        path('', master_kategori.Master_kategoriViews.as_view(), name = 'master_kategori'),
        path('add', master_kategori.AddCategory.as_view(), name = 'add_kategori'),
        path('edit/<str:categori_id>', master_kategori.EditCategory.as_view(), name = 'edit_kategori'),
        path('del/<str:categori_id>', master_kategori.DeleteCategory.as_view(), name = 'del_kategori'),
        path('delete_at/<str:categori_id>/',Delete_at_kategori.as_view(),name='delete_at_kategori'),
        path('histori/',master_kategori.Historikategori.as_view(),name='histori_kategori'),
        path('restore/<str:categori_id>/',master_kategori.Restorekategori.as_view(),name='restore_kategori'),
        
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
        path('add_kontak/',admin_kontak.Addkontak.as_view(),name='add_kontak'),
        path('edit_kontak/<str:id>', admin_kontak.Editkontak.as_view(),name='edit_kontak'),
        path('delete/<str:id>', admin_kontak.Deletekontak.as_view(),name='delete_kontak'),
        ])),
    
    path('master_wilayah/',include([
        path('', master_wilayah.Master_wilayahViews.as_view(), name = 'master_wilayah'),
        path('add/', master_wilayah.AddWilayah.as_view(), name = 'add_wilayah'),
        path('edit/<str:wilayah_id>/',master_wilayah.EditWilayah.as_view(), name='edit_wilayah'),
        path('delete/<str:wilayah_id>/', master_wilayah.DeleteWilayah.as_view(), name = 'delete_wilayah'),
       
        ])),
    
    path('master_sarpras/',include([
        path('', master_sarpras.Master_kategoriViews.as_view(), name = 'master_sarpras'),
        path('add/', master_sarpras.AddSarpras.as_view(), name = 'add_master_sarpras'),
        path('edit/<str:id>/',master_sarpras.EditSarpras.as_view(), name ='edit_master_sarpras'),
        path('delete/<str:id>/', master_sarpras.DeleteSarpras.as_view(), name='delete_master_sarpras')
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
        path('delete_slider/<str:id_slider>',master_slider.Delete_slider.as_view(),name='delete_slider'),
        path('edit/<str:id_slider>', master_slider.Editslider.as_view(), name = 'edit_slider'),
        path('delete_at/<str:id_slider>/',Delete_at_slider.as_view(),name='delete_at_slider'),
        path('histori/',master_slider.Historislider.as_view(),name='histori_slider'),
        path('restore/<str:id_slider>/',master_slider.Restoreslider.as_view(),name='restore_slider'),
        ])),

    path('master_jenis_kesehatan/',include([
        path('',master_jenis_kesehatan.Master_jenis_kesehatanView.as_view(),name='master_jenis_kesehatan'),
        path('add_jenis_kesehatan',master_jenis_kesehatan.Add_jenis_kesehatan.as_view(),name='add_jenis_kesehatan'),
        path('edit/<str:jenis_kesehatan_id>',master_jenis_kesehatan.Edit_jenis_kesehatan.as_view(),name='edit_jenis_kesehatan'),
        path('delete/<str:jenis_kesehatan_id>',master_jenis_kesehatan.Deletejenis_kesehatan.as_view(),name='delete_jenis_kesehatan'),
        path('delete_at/<str:jenis_kesehatan_id>/',Delete_at_jenis_kesehatan.as_view(),name='delete_at_jenis_kesehatan'),
        path('histori/',master_jenis_kesehatan.Historijenis_kesehatan.as_view(),name='histori_jenis_kesehatan'),
        path('restore/<str:jenis_kesehatan_id>/',master_jenis_kesehatan.Restorejenis_kesehatan.as_view(),name='restore_jenis_kesehatan'),

        path('indikator/<str:jenis_kesehatan_id>',master_indikator.Master_indikator.as_view(),name='master_indikator'),
        path('add_indikator',master_indikator.Add_indikator.as_view(),name='add_indikator'),
        path('edit_indikator/<str:id_indikator>',master_indikator.Edit_indikator.as_view(),name='edit_idikator'),
        path('indikator/delete_indikator/<str:id_indikator>',master_indikator.Delete_indikator.as_view(),name='delete_indikator'),

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
        path('add_info_wilayah/<str:wilayah_id>/',admin_info_wilayah.FormWilayah.as_view(),name='add_info_wilayah'),
        path('info_wilayah_add',admin_info_wilayah.InfoWilayahAdd.as_view(),name='info_wilayah_add'),
        path('info_wilayah_edit/<str:wilayah_id>/',admin_info_wilayah.EditInfoWilayah.as_view(),name='edit_info_wilayah'),
        
        path('add_sarpras/',admin_info_wilayah.Addsarpras.as_view(),name='add_sarpras'),
        
        path('detail/<str:wilayah_id>/',admin_info_wilayah.Detail_info_wilayah.as_view(),name='detail_info_wilayah'),
        path('delete/<str:wilayah_id>/', master_wilayah.DeleteWilayah.as_view(), name = 'delete_wilayah'),
        ])),

    path('data_kesehatan/',include([
        path('',admin_data_kesehatan.Admin_data_kesehatanViews.as_view(),name='data_kesehatan'),
        path('pilih_wilayah/',admin_data_kesehatan.Pilih_wilayah.as_view(),name='pilih_wilayah'),
        path('detail/<str:jenis_kesehatan_id>',admin_data_kesehatan.Detail_data_kesehatanViews.as_view(),name='detail_data_kesehatan'),    
           
        path('add',admin_data_kesehatan.Add_data_kesehatan.as_view(),name='add_data_kesehatan'),
        path('delete/<str:data_kesehatan_id>/', admin_data_kesehatan.DeleteKesehatan.as_view(), name = 'delete_kesehatan'),
        path('delete_at/<str:data_kesehatan_id>/',Delete_at_kesehatan.as_view(),name='delete_at_kesehatan'),
        path('histori/',admin_data_kesehatan.Historikesehatan.as_view(),name='histori_kesehatan'),
        path('restore/<str:data_kesehatan_id>/',admin_data_kesehatan.Restorekesehatan.as_view(),name='restore_kesehatan'),
        ])),

    path('data_penduduk/',include([
         path('',admin_data_penduduk.Admin_data_pendudukViews.as_view(),name='data_penduduk'),
         path('add/',admin_data_penduduk.Add_data_penduduk.as_view(),name='add_data_penduduk'),
         path('semua/',admin_data_penduduk.Semua_data.as_view(),name='semua_penduduk'),
         path('detail/<str:wilayah_id>/',admin_data_penduduk.Detail_penduduk.as_view(),name='detail_data_penduduk'),
         path('edit/<str:data_penduduk_id>/', admin_data_penduduk.edit_data_penduduk.as_view(), name = 'edit_data_penduduk'),
         path('delete/<str:data_penduduk_id>/', admin_data_penduduk.DeletePenduduk.as_view(), name = 'delete_penduduk'),
         
         ])),

    path('kontak/',include([
        path('',admin_kontak.Admin_kontakViews.as_view(),name='admin_kontak'),
        path('add_kontak/',admin_kontak.Addkontak.as_view(),name='add_kontak'),
        path('edit_kontak/<str:id>',admin_kontak.Editkontak.as_view(),name='edit_kontak'),
      
        ])),

    path('tentang_kami/',include([
         path('',admin_tentang.Admin_tetang_kami.as_view(),name='admin_tentang'),
         path('add_tentang/',admin_tentang.Add_tentang.as_view(),name='add_tentang'),
         path('edit_tentang/<str:id_tentang>',admin_tentang.Edittentang.as_view(),name='edit_tentang'),
        ])),

]
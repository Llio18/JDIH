from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('kategori/<slug:imput>/', views.kategori_view, name='kategori_view'),
    path('detail/<slug:imput>/', views.detail_view, name='detail_view'),
    path('detail/<slug:imput>/download/',
         views.unduh_dokumen, name='unduh_dokumen'),
    path('dokumen', views.dokumen, name='semua_dokumen')
]

# path('test/', views.testing, name='testing'),

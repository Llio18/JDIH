from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('keputusan/', views.keputusan_view, name='keputusan'),

    path('peraturan/', views.peraturan_view, name='peraturan'),

    path('artikel/', views.artikel_view, name='artikel'),

    path('dokumen_lain/', views.dokumenLain_view, name='dokumen_lain'),
]

from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('kategori/<slug:imput>/', views.kategori_view, name='kategori_view'),
]

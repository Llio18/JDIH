from ast import Return
from django.shortcuts import render

# Create your views here.


def index(request):

    # context = {
    #     'heading': 'Hallo gess selamat datang di website  Jdih Unima',
    # }
    return render(request, 'index.html')


# View untuk menampilkan halaman Keputusan Pimpinan
def keputusan_view(request):
    return render(request, 'JDIH/keputusan.html')

# View untuk menampilkan halaman Peraturan
def peraturan_view(request):
    return render(request, 'JDIH/peraturan.html')

# View untuk menampilkan halaman Artikel Hukum 
def artikel_view(request):
    return render(request, 'JDIH/artikel.html')

# View untuk menampilkan halaman Monografi Hukum
def monografi_view(request):
    return render(request, 'JDIH/monografi.html')

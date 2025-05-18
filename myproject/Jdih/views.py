from ast import Return
from multiprocessing import context
from django.shortcuts import redirect, render
from .form import FormKontak
from .models import DokumenHukum

# Create your views here.


def index(request):

    daftar_dokumen = DokumenHukum.objects.all()[:8]

    if request.method == 'POST':
        f_kontak = FormKontak(request.POST or None)
        if f_kontak.is_valid():
            f_kontak.save()

            return redirect('index')

    else:
        f_kontak = FormKontak()

    context = {
        'f_kontak': f_kontak,
        'daftar_dokumen': daftar_dokumen,
    }

    return render(request, 'index.html', context)


# View untuk menampilkan halaman Keputusan Pimpinan
def keputusan_view(request):
    daftar_artikel = DokumenHukum.objects.filter(kategori__nama='Keputusan Pimpinan')
    return render(request, 'JDIH/artikel.html', {'daftar_artikel': daftar_artikel})

# View untuk menampilkan halaman Peraturan


def peraturan_view(request):
    daftar_artikel = DokumenHukum.objects.filter(kategori__nama='Peraturan')
    return render(request, 'JDIH/artikel.html', {'daftar_artikel': daftar_artikel})

# View untuk menampilkan halaman Artikel Hukum


def artikel_view(request):

    daftar_artikel = DokumenHukum.objects.filter(kategori__nama='Artikel Hukum')
    return render(request, 'JDIH/artikel.html', {'daftar_artikel': daftar_artikel})

# View untuk menampilkan halaman Monografi Hukum

def dokumenLain_view(request):
    daftar_artikel = DokumenHukum.objects.filter(kategori__nama='Dokumen Lain')
    return render(request, 'JDIH/dokumen_lain.html', {'daftar_artikel': daftar_artikel})

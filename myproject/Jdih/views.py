from ast import Return
from multiprocessing import context
from webbrowser import get
from django.shortcuts import redirect, render, get_object_or_404
from .form import FormKontak
from .models import DokumenHukum, KategoriDokumen
from django.db.models import Count
from django.db.models import Q
# Create your views here.


def index(request):

    query = request.GET.get('cari')

    hitung_kategori = KategoriDokumen.objects.annotate(
        jumlah_dokumen=Count('dokumenhukum')
    ).order_by('nama')

    # daftar_dokumen = DokumenHukum.objects.all()[:12]

    if query:
        daftar_dokumen = DokumenHukum.objects.filter(
            Q(judul__icontains=query) |
            Q(nomor__icontains=query) |
            Q(isi_teks__icontains=query) |
            Q(kategori__nama__icontains=query)
        ).order_by('-tahun')
    else:
        daftar_dokumen = DokumenHukum.objects.all()[:12]

    if request.method == 'POST':
        f_kontak = FormKontak(request.POST or None)
        if f_kontak.is_valid():
            f_kontak.save()

            return redirect('index')

    else:
        f_kontak = FormKontak()

    context = {
        'hitung_kategori': hitung_kategori,
        'f_kontak': f_kontak,
        'daftar_dokumen': daftar_dokumen,
        'query': query,
    }

    return render(request, 'index.html', context)


# View Untuk halama kategori agar dinamis

def kategori_view(request, imput):
    kategori = get_object_or_404(KategoriDokumen, slug=imput)
    daftar_dokumen = DokumenHukum.objects.filter(kategori=kategori)

    context = {
        'kategori': kategori,
        'daftar_dokumen': daftar_dokumen,
        'kategori_aktif': imput,
    }

    return render(request, 'JDIH/kategori.html', context)

# View untuk menampilkan halaman Keputusan Pimpinan

# def keputusan_view(request):
#     daftar_dokumen = DokumenHukum.objects.filter(
#         kategori__nama='Keputusan Rektor')
#     context = {
#         'keputusan_pimpinan': daftar_dokumen,
#     }
#     return render(request, 'JDIH/keputusan.html', context)

# # View untuk menampilkan halaman Peraturan


# def peraturan_view(request):
#     daftar_peraturan = DokumenHukum.objects.filter(kategori__nama='Peraturan')
#     context = {
#         'daftar_peraturan': daftar_peraturan,
#     }
#     return render(request, 'JDIH/peraturan.html', context)

# # View untuk menampilkan halaman Artikel Hukum


# def artikel_view(request):

#     daftar_artikel = DokumenHukum.objects.filter(
#         kategori__nama='Artikel')
#     context = {
#         'daftar_artikel': daftar_artikel,
#     }
#     return render(request, 'JDIH/artikel.html', context)

# # View untuk menampilkan halaman Monografi Hukum


# def dokumenLain_view(request):
#     daftar_artikel = DokumenHukum.objects.filter(kategori__nama='Dokumen Lain')
#     return render(request, 'JDIH/dokumen_lain.html', {'daftar_artikel': daftar_artikel})


from django.shortcuts import render, redirect, get_object_or_404
from .form import FormKontak
from .models import DokumenHukum, KategoriDokumen
from django.db.models import Count
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def index(request):
    query = request.GET.get('cari')
    search_type = request.GET.get('search_type', 'regular')

    show_all = request.GET.get('show') == 'all'

    if query:
        if search_type == 'binary':
            hasil_pencarian = DokumenHukum.cari_binary_search(query)
            is_binary = True
        else:
            # Hasilnya adalah sebuah QUERYSET
            hasil_pencarian = DokumenHukum.objects.filter(
                Q(judul__icontains=query) |
                Q(nomor__icontains=query) |
                Q(kategori__nama__icontains=query)
            ).order_by('-tahun')
            is_binary = False

        show_all = True
    else:
        is_binary = False
        if show_all:
            hasil_pencarian = DokumenHukum.objects.all()
        else:
            hasil_pencarian = DokumenHukum.objects.all()[:12]

    page_obj = None
    if show_all:
        paginator = Paginator(hasil_pencarian, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    hitung_kategori = KategoriDokumen.objects.annotate(
        jumlah_dokumen=Count('dokumenhukum')
    ).order_by('nama')

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
        'page_obj': page_obj,
        'query': query,
        'is_binary': is_binary,
        'show_all': show_all,
        'dokumen_list': page_obj if show_all else hasil_pencarian,
    }

    return render(request, 'index.html', context)


# View Untuk halama kategori agar dinamis
def kategori_view(request, imput):
    query = request.GET.get('cari')
    search_type = request.GET.get('search_type', 'regular')
    kategori = get_object_or_404(KategoriDokumen, slug=imput)
    show_all = request.GET.get('show') == 'all'
    is_binary = False

    if query:
        if search_type == 'binary':
            hasil_pencarian = DokumenHukum.cari_binary_search(
                query, kategori_slug=imput
            )
            is_binary = True
        else:
            hasil_pencarian = DokumenHukum.objects.filter(kategori=kategori).filter(
                Q(judul__icontains=query) |
                Q(nomor__icontains=query)
            ).order_by('-tahun')

        show_all = True
    else:
        hasil_pencarian = DokumenHukum.objects.filter(
            kategori=kategori
        ).order_by('-tahun')

    page_obj = None
    if show_all:
        paginator = Paginator(hasil_pencarian, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        daftar_dokumen = page_obj
    else:
        daftar_dokumen = hasil_pencarian[:12]

    context = {
        'kategori': kategori,
        'daftar_dokumen': daftar_dokumen,
        'kategori_aktif': imput,
        'page_obj': page_obj,
        'show_all': show_all,
        'query': query,
        'is_binary': is_binary,
        'search_type': search_type,
    }

    return render(request, 'JDIH/kategori.html', context)


# view untuk halaman detail
def detail_view(request, imput):
    dokumen = DokumenHukum.objects.get(slug=imput)

    context = {
        'dokumen': dokumen,
    }

    return render(request, 'JDIH/detail_view.html', context)


# view untuk halaman seluruh dokumen
def dokumen(request):
    return render(request, 'JDIH/dokumen.html')

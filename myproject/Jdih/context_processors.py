from .models import KategoriDokumen


def kategori_navbar(request):
    """
    for navbar dropdown menu Dokumen Hukum dan footer
    """
    kategori_navbar = KategoriDokumen.objects.all().order_by('nama')
    return {
        'daftar_kategori': kategori_navbar,
    }
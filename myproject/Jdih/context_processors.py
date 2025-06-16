from .models import KategoriDokumen

def kategori_navbar(request):
    """
    for navbar dropdown menu Dokumen Hukum
    """
    kategori_navbar = KategoriDokumen.objects.all().exclude(nama="Dummy").order_by('nama')
    return {
        'daftar_kategori': kategori_navbar,
    }
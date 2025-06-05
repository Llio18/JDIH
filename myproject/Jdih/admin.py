from atexit import register
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import  DokumenHukum, KategoriDokumen, Kontak


@admin.register(DokumenHukum)
class CustomAdminClass(ModelAdmin):
    list_display = ('nomor', 'judul', 'tahun', 'tanggal_ditetapkan', 'kategori')


@admin.register(KategoriDokumen)
class CustomAdminClass(ModelAdmin):
    pass



@admin.register(Kontak)
class CustomAdminClass(ModelAdmin):
    list_display = ('nama', 'email', 'pesan','tanggal') 
    readonly_fields = ('tanggal',)  


# admin.site.register(KategoriDokumen)

# @admin.register(Kontak)
# class KontakAdmin(admin.ModelAdmin):
#     list_display = ('nama', 'email', 'pesan','tanggal')  # Tambahkan 'tanggal' di sini
#     readonly_fields = ('tanggal',)  # Biarkan field ini read-only
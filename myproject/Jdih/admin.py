from atexit import register
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import DokumenHukum, KategoriDokumen, Kontak
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm
from .resources import DokumenHukumResource


@admin.register(DokumenHukum)
class CustomAdminClass(ModelAdmin, ImportExportModelAdmin):

    resource_class = DokumenHukumResource

    list_display = ('nomor', 'judul', 'tahun',
                    'tanggal_ditetapkan', 'kategori')
    search_fields = ('judul', 'nomor', 'tahun', 'kategori__nama')
    export_form_class = ExportForm
    import_form_class = ImportForm


@admin.register(KategoriDokumen)
class CustomAdminClass(ModelAdmin):
    pass


@admin.register(Kontak)
class CustomAdminClass(ModelAdmin):
    list_display = ('nama', 'email', 'pesan', 'tanggal')
    readonly_fields = ('tanggal',)


# admin.site.register(KategoriDokumen)

# @admin.register(Kontak)
# class KontakAdmin(admin.ModelAdmin):
#     list_display = ('nama', 'email', 'pesan','tanggal')  # Tambahkan 'tanggal' di sini
#     readonly_fields = ('tanggal',)  # Biarkan field ini read-only

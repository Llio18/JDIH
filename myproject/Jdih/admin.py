from django.contrib import admin

# Register your models here.
from .models import KategoriDokumen, DokumenHukum

admin.site.register(KategoriDokumen)
admin.site.register(DokumenHukum)

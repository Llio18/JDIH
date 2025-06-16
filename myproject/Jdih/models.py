from csv import reader
from enum import unique
from django.db import models
from django.utils.text import slugify
from PyPDF2 import PdfReader
from django.core.files import File
# Create your models here.


class KategoriDokumen(models.Model):
    nama = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nama)
        return super(KategoriDokumen, self).save(*args, **kwargs)

    def __str__(self):
        return self.nama


class DokumenHukum(models.Model):
    nomor = models.CharField("Nomor Dokumen", max_length=100)
    judul = models.TextField("Judul")
    tahun = models.PositiveIntegerField("Tahun Terbit")
    tanggal_ditetapkan = models.DateField("Tanggal Ditetapkan")
    kategori = models.ForeignKey(
        KategoriDokumen, on_delete=models.SET_NULL, null=True, blank=True)
    file_pdf = models.FileField("File Dokumen", upload_to='')
    isi_teks = models.TextField(
        "Isi Teks", blank=True, help_text="Teks ekstrak dari PDF")

    class Meta:
        ordering = ['-tahun', 'judul']

    def __str__(self):
        return f"{self.judul} ({self.nomor})"

    def save(self, *args, **kwargs):

        is_new_pdf = False
        if self.file_pdf:
            if not self.pk:
                is_new_pdf = True
            else:
                old_pdf = DokumenHukum.objects.get(pk=self.pk).file_pdf
                if old_pdf != self.file_pdf:
                    is_new_pdf = True

        super().save(*args, **kwargs)

        if is_new_pdf:
            try:
                reader = PdfReader(self.file_pdf.path)
                self.isi_teks = "\n".join(
                    page.extract_text()
                    for page in reader.pages
                    if page.extract_text()
                )
            except Exception as e:
                print(f"Error extracting PDF: {e}")
                self.isi_teks = ""

        super().save(*args, **kwargs)


class Kontak(models.Model):
    nama = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    pesan = models.TextField()
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"pesan dari {self.nama}"

from django.db import models

# Create your models here.


class KategoriDokumen(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama


class DokumenHukum(models.Model):
    nomor = models.CharField("Nomor Dokumen", max_length=100)
    judul = models.TextField("Judul")
    tahun = models.PositiveIntegerField("Tahun Terbit")
    tanggal_ditetapkan = models.DateField("Tanggal Ditetapkan")
    kategori = models.ForeignKey(
        KategoriDokumen, on_delete=models.SET_NULL, null=True, blank=True)
    file_pdf = models.FileField("File Dokumen", upload_to='dokumen/')
    isi_teks = models.TextField(
        "Isi Teks", blank=True, help_text="Teks hasil ekstrak dari file PDF")

    class Meta:
        ordering = ['-tahun', 'judul']

    def __str__(self):
        return f"{self.judul} ({self.nomor})"

from csv import reader
from enum import unique
from zipfile import LargeZipFile
from django.db import models
from django.utils.text import slugify
from PyPDF2 import PdfReader
from django.core.files import File
import re
from bisect import bisect_left, bisect_right
# Create your models here.


class KategoriDokumen(models.Model):
    nama = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)

    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        old_name = None
        if self.pk:
            try:
                old_instance = KategoriDokumen.objects.get(pk=self.pk)
                old_name = old_instance.nama
            except KategoriDokumen.DoesNotExist:
                pass  # Objek tidak ditemukan

        if self.nama != old_name or not self.slug:
            base_slug = slugify(self.nama)
            slug = base_slug
            n = 0
            while KategoriDokumen.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f"{base_slug}-{n}"
            self.slug = slug

        super().save(*args, **kwargs)


class DokumenHukum(models.Model):
    nomor = models.CharField("Nomor Dokumen", max_length=100)
    judul = models.TextField("Judul")
    tahun = models.PositiveIntegerField("Tahun Terbit")
    tanggal_ditetapkan = models.DateField("Tanggal Ditetapkan")
    kategori = models.ForeignKey(
        KategoriDokumen, on_delete=models.SET_NULL, null=True, blank=True)
    file_pdf = models.FileField("File Dokumen", upload_to='dokumen_hukum/')
    isi_teks = models.TextField(
        "Isi Teks", blank=True, help_text="Teks ekstrak dari PDF")
    slug = models.SlugField(max_length=100, blank=True, unique=True)

    class Meta:
        ordering = ['-tahun', 'judul']

    def __str__(self):
        return f"{self.judul} ({self.nomor})"

    def save(self, *args, **kwargs):
        # 1. Hasilkan slug
        if not self.slug:
            self.slug = slugify(self.judul)

        # 2. Ekstrak teks dari file PDF jika ada
        if self.file_pdf:
            try:
                reader = PdfReader(self.file_pdf)
                extracted_text = "\n".join(
                    page.extract_text() for page in reader.pages if page.extract_text()
                )
                self.isi_teks = extracted_text
            except Exception as e:
                print(f"Error extracting PDF text for '{self.judul}': {e}")
                self.isi_teks = ""

        # 3. Simpan semua perubahan ke database
        super().save(*args, **kwargs)

    @classmethod
    def cari_binary_search(cls, query):
        results = []

        for dokumen in cls.objects.all():
            kata_kata = re.findall(r'\w+', dokumen.isi_teks.lower())

            kata_terurut = sorted(kata_kata)

            query = query.lower().strip()
            left = bisect_left(kata_terurut, query)
            right = bisect_right(kata_terurut, query)
            freq = right - left

            if freq > 0:
                results.append({
                    'dokumen': dokumen,
                    'frekuensi': freq,
                    'slug': dokumen.slug,
                    'kategori': dokumen.kategori.nama if dokumen.kategori else ''
                })
        return sorted(results, key=lambda x: -x['frekuensi'])


class Kontak(models.Model):
    nama = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    pesan = models.TextField()
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"pesan dari {self.nama}"

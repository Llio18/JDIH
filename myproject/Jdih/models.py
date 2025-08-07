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
    tanggal_ditetapkan = models.DateField(
        "Tanggal Ditetapkan",
        null=True,
        blank=True,
    )
    kategori = models.ForeignKey(
        KategoriDokumen,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    file_pdf = models.FileField(
        "File Dokumen",
        upload_to='dokumen_hukum/',
        max_length=225,
    )
    isi_teks = models.TextField(
        "Isi Teks", blank=True, help_text="Teks ekstrak dari PDF")
    slug = models.SlugField(max_length=225, blank=True, unique=True)

    class Meta:
        ordering = ['-tahun', 'judul']

    def __str__(self):
        return f"{self.judul} ({self.nomor})"

    def save(self, *args, **kwargs):

        if not self.slug or self.judul != getattr(DokumenHukum.objects.filter(pk=self.pk).first(), 'judul', None):

            base_slug = slugify(self.judul)

            max_len = self._meta.get_field('slug').max_length

            slug = base_slug[:max_len]

            n = 0
            while DokumenHukum.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                sisa_ruang = max_len - len(str(n)) - 1
                slug = f"{base_slug[:sisa_ruang]}-{n}"

            self.slug = slug

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
    def cari_binary_search(cls, query, kategori_slug=None):
        results = []

        semua_dokumen = cls.objects.all()

        if kategori_slug:
            semua_dokumen = semua_dokumen.filter(kategori__slug=kategori_slug)

        for dokumen in semua_dokumen:
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

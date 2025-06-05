import os
import logging
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import DokumenHukum
# from PyPDF2 import PdfReader
# from django.db import transaction


logger = logging.getLogger(__name__)
# --- Sinyal untuk Hapus File PDF ---


@receiver(post_delete, sender=DokumenHukum)
def hapus_file_dokumen(sender, instance, **kwargs):
    if instance.file_pdf:
        file_path = instance.file_pdf.path
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                logger.info(f"File {file_path} telah dihapus.")
            except Exception as e:
                logger.error(f"Gagal menghapus file {file_path}: {e}")
        else:
            logger.warning(f"File {file_path} tidak ditemukan.")


# --- Sinyal untuk Ekstrak Teks dari PDF ---
# _changed_instance = {}


# @receiver(pre_save, sender=DokumenHukum)
# def cek__file_pdf_berubah(sender, instance, **kwargs):
#     key = instance.pk or id(instance)
#     if not instance.pk:
#         _changed_instance[key] = True
#     else:
#         try:
#             old = DokumenHukum.objects.get(pk=instance.pk)
#             # Bandingkan nama file, bukan objek FileField
#             _changed_instance[key] = old.file_pdf.name != instance.file_pdf.name
#         except DokumenHukum.DoesNotExist:
#             _changed_instance[key] = True


# @receiver(post_save, sender=DokumenHukum)
# def ekstrak_teks_pdf(sender, instance, created, **kwargs):
#     key = instance.pk or id(instance)
#     is_new_pdf = _changed_instance.pop(key, False)

#     if is_new_pdf and instance.file_pdf and hasattr(instance.file_pdf, 'path'):
#         def proses_ekstraksi():
#             print("[INFO] Memulai ekstraksi teks setelah commit DB.")
#             try:
#                 path = instance.file_pdf.path
#                 print(f"[DEBUG] Path file PDF: {path}")
#                 if not os.path.exists(path):
#                     print("[ERROR] File PDF belum tersedia di disk.")
#                     return

#                 reader = PdfReader(path)
#                 text = "\n".join(
#                     page.extract_text() for page in reader.pages if page.extract_text()
#                 )
#                 print(f"[DEBUG] Ekstrak berhasil. Teks awal:\n{text[:100]}...")
#             except Exception as e:
#                 print(f"[ERROR] Gagal ekstrak PDF: {e}")
#                 text = ""

#             # Update field tanpa trigger sinyal lagi
#             instance.isi_teks = text
#             sender.objects.filter(pk=instance.pk).update(isi_teks=text)

#         transaction.on_commit(proses_ekstraksi)
#     else:
#         print("[INFO] PDF tidak berubah, ekstraksi dilewati.")

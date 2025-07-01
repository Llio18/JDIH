
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import DokumenHukum, KategoriDokumen


class DokumenHukumResource(resources.ModelResource):

    kategori = fields.Field(
        column_name='kategori',
        attribute='kategori',
        widget=ForeignKeyWidget(KategoriDokumen, 'nama'))

    class Meta:
        model = DokumenHukum
        # Sertakan 'kategori' yang baru kita definisikan di atas
        fields = ('id', 'nomor', 'judul', 'tahun',
                  'tanggal_ditetapkan', 'kategori', 'file_pdf',)

    def skip_row(self, instance, original, row, import_validation_errors=None):
        # Jika kolom 'judul' kosong atau tidak ada, lewati baris ini
        if not row.get('judul'):
            return True
        return super().skip_row(instance, original, row, import_validation_errors)

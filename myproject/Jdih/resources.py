
from import_export import resources
from .models import DokumenHukum


class DokumenHukumResource(resources.ModelResource):
    class Meta:
        model = DokumenHukum
        fields = ('id', 'nomor', 'judul', 'tahun',
                  'tanggal_ditetapkan', 'kategori', 'file_pdf',)

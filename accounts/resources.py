# Example: resources.py

from import_export import resources
from .models import Kategori, PosisiAsset, AsetBaru, DetailAset, Pembelian, Lampiran, PenanggungJawab

class AsetBaruResource(resources.ModelResource):
    class Meta:
        model = AsetBaru
        fields = ('nama_aset', 'kode_aset', 'kategori__nama', 'kondisi_aset', 'posisi_aset__lokasi')

class KategoriResource(resources.ModelResource):
    class Meta:
        model = Kategori
        fields = ('nama',)

class PosisiAssetResource(resources.ModelResource):
    class Meta:
        model = PosisiAsset


class DetailAsetResource(resources.ModelResource):
    class Meta:
        model = DetailAset

class PembelianResource(resources.ModelResource):
    class Meta:
        model = Pembelian

class LampiranResource(resources.ModelResource):
    class Meta:
        model = Lampiran

class PenanggungJawabResource(resources.ModelResource):
    class Meta:
        model = PenanggungJawab

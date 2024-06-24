from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Kategori, PosisiAsset, AsetBaru, DetailAset, Pembelian, Lampiran, PenanggungJawab

class KategoriResource(resources.ModelResource):
    class Meta:
        model = Kategori

class PosisiAssetResource(resources.ModelResource):
    class Meta:
        model = PosisiAsset

class AsetBaruResource(resources.ModelResource):
    class Meta:
        model = AsetBaru

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

# Integrasi resource dengan model admin
class KategoriAdmin(ImportExportModelAdmin):
    resource_class = KategoriResource

class PosisiAssetAdmin(ImportExportModelAdmin):
    resource_class = PosisiAssetResource

class AsetBaruAdmin(ImportExportModelAdmin):
    resource_class = AsetBaruResource

class DetailAsetAdmin(ImportExportModelAdmin):
    resource_class = DetailAsetResource

class PembelianAdmin(ImportExportModelAdmin):
    resource_class = PembelianResource

class LampiranAdmin(ImportExportModelAdmin):
    resource_class = LampiranResource

class PenanggungJawabAdmin(ImportExportModelAdmin):
    resource_class = PenanggungJawabResource

# Register model admin ke Django admin site
admin.site.register(Kategori, KategoriAdmin)
admin.site.register(PosisiAsset, PosisiAssetAdmin)
admin.site.register(AsetBaru, AsetBaruAdmin)
admin.site.register(DetailAset, DetailAsetAdmin)
admin.site.register(Pembelian, PembelianAdmin)
admin.site.register(Lampiran, LampiranAdmin)
admin.site.register(PenanggungJawab, PenanggungJawabAdmin)

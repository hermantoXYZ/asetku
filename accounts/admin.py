from django.contrib import admin
from .models import User
from .models import AsetBaru, DetailAset, Pembelian, Lampiran, Kategori, PenanggungJawab

# Register your models here.

admin.site.register(User)

@admin.register(AsetBaru)
class AsetBaruAdmin(admin.ModelAdmin):
    pass  # Jika ingin menggunakan pengaturan default

@admin.register(DetailAset)
class DetailAsetAdmin(admin.ModelAdmin):
    pass

@admin.register(Pembelian)
class PembelianAdmin(admin.ModelAdmin):
    pass

@admin.register(Lampiran)
class LampiranAdmin(admin.ModelAdmin):
    pass

# @admin.register(Penyusutan)
# class PenyusutanAdmin(admin.ModelAdmin):
#     pass

@admin.register(PenanggungJawab)
class PenanggungJawabAdmin(admin.ModelAdmin):
    pass

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    pass
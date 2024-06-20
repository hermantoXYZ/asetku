# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid

class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_staff = models.BooleanField('Is staff', default=False)
    is_user = models.BooleanField('Is user', default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.username
    
class Kategori(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama
    


class AsetBaru(models.Model):
    nama_aset = models.CharField(max_length=255)
    kode_aset = models.CharField(max_length=50, blank=True, null=True)
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)

    def __str__(self):
        return self.nama_aset

    def generate_kode_aset(self):
        current_date = timezone.now().date()
        current_year = current_date.year
        current_month = current_date.month
        current_day = current_date.day
        prefix = "ENV"
        unique_id = uuid.uuid4().hex[:6]  # Mendapatkan 6 karakter pertama dari UUID dalam bentuk hex

        return f"{unique_id}/{prefix}/{current_day}/{current_month}/{current_year}"

    def save(self, *args, **kwargs):
        if not self.kode_aset:
            self.kode_aset = self.generate_kode_aset()
        super(AsetBaru, self).save(*args, **kwargs)

    
class DetailAset(models.Model):

    TAHUN_PRODUKSI_CHOICES = [
        (year, year) for year in range(2000, 2025)  # Contoh range tahun dari 2000 sampai 2024
    ]
     
    aset = models.OneToOneField(AsetBaru, on_delete=models.CASCADE, related_name='detail')
    merk = models.CharField(max_length=100)
    tipe = models.CharField(max_length=100)
    produsen = models.CharField(max_length=100)
    no_seri_kode_produksi = models.CharField(max_length=50)
    tahun_produksi = models.PositiveIntegerField(choices=TAHUN_PRODUKSI_CHOICES)
    deskripsi = models.TextField()

    def __str__(self):
        return f"Detail {self.aset.nama_aset}"
    
class Pembelian(models.Model):
    aset = models.ForeignKey(AsetBaru, on_delete=models.CASCADE, related_name='pembelian')
    tanggal_pembelian = models.DateField()
    toko_distributor = models.CharField(max_length=255)
    no_invoice = models.CharField(max_length=50)
    jumlah = models.PositiveIntegerField()
    harga_satuan = models.DecimalField(max_digits=12, decimal_places=1)
    harga_total = models.DecimalField(max_digits=15, decimal_places=1)

    def save(self, *args, **kwargs):
        # Hitung harga_total berdasarkan harga_satuan dan jumlah
        self.harga_total = self.harga_satuan * self.jumlah
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Pembelian {self.aset.nama_aset}"
    
class Lampiran(models.Model):
    aset = models.ForeignKey(AsetBaru, on_delete=models.CASCADE, related_name='lampiran')
    foto = models.FileField(upload_to='lampiran/')
    keterangan = models.TextField(blank=True)

    def __str__(self):
        return f"Lampiran {self.aset.nama_aset}"
    

class PenanggungJawab(models.Model):
    aset = models.ForeignKey(AsetBaru, on_delete=models.CASCADE, related_name='penanggung_jawab')
    nama = models.CharField(max_length=255)
    jabatan = models.CharField(max_length=255)

    def __str__(self):
        return self.nama


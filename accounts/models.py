# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid

import os
from django.utils.text import slugify
from datetime import datetime
import random

def rename_image(instance, filename):
    upload_to = 'images/'
    ext = filename.split('.')[-1]
    
    current_date = datetime.now().strftime('%Y_%m_%d')
    random_number = random.randint(100000, 999999)  # Generate a 6-digit random number
    
    if hasattr(instance, 'judul') and instance.judul:
        filename = f"{slugify(instance.judul)}_{current_date}_{random_number}.{ext}"
    elif hasattr(instance, 'title') and instance.title:
        filename = f"{slugify(instance.title)}_{current_date}_{random_number}.{ext}"
    elif instance.pk:
        filename = f"{instance.pk}_{current_date}_{random_number}.{ext}"
    else:
        filename = f"{current_date}_{random_number}.{ext}"
    
    return os.path.join(upload_to, filename)


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
    
class PosisiAsset(models.Model):
    lokasi = models.CharField(max_length=100)

    def __str__(self):
        return self.lokasi
    
KONDISI_CHOICES = (
    ('Baik', 'Baik'),
    ('Rusak', 'Rusak'),
    ('Rusak Berat', 'Rusak Berat'),
)

class AsetBaru(models.Model):
    nama_aset = models.CharField(max_length=255)
    kode_aset = models.CharField(max_length=50, blank=True, null=True)
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    kondisi_aset = models.CharField(max_length=12, choices=KONDISI_CHOICES, default='baik')
    posisi_aset = models.ForeignKey(PosisiAsset, on_delete=models.SET_NULL, null=True, blank=True)

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
    tanggal_kontrak = models.DateField()
    toko_distributor = models.CharField(max_length=255)
    no_kontrak = models.CharField(max_length=50)
    unit = models.PositiveIntegerField()
    harga_satuan = models.DecimalField(max_digits=12, decimal_places=1)
    harga_total = models.DecimalField(max_digits=15, decimal_places=1)

    def save(self, *args, **kwargs):
        # Hitung harga_total berdasarkan harga_satuan dan jumlah
        self.harga_total = self.harga_satuan * self.unit
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Pembelian {self.aset.nama_aset}"
    
class Lampiran(models.Model):
    aset = models.ForeignKey(AsetBaru, on_delete=models.CASCADE, related_name='lampiran')
    foto = models.FileField(upload_to=rename_image, blank=True, null=True)
    keterangan = models.TextField(blank=True)

    def __str__(self):
        return f"Lampiran {self.aset.nama_aset}"
    

class PenanggungJawab(models.Model):
    aset = models.ForeignKey(AsetBaru, on_delete=models.CASCADE, related_name='penanggung_jawab')
    nama = models.CharField(max_length=255)
    jabatan = models.CharField(max_length=255)

    def __str__(self):
        return self.nama


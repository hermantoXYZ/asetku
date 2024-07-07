# models.py
from io import BytesIO
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid

import os
from django.utils.text import slugify
from datetime import datetime
import random

from io import BytesIO
import qrcode
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile 
from urllib.parse import urlparse
from django.urls import reverse

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

        return f"{unique_id}/{prefix}/{current_day}_{current_month}_{current_year}"

    def generate_qr_code(self, detail_url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(detail_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill='black', back_color='white').convert('RGB')

        font = ImageFont.load_default()
        text = f"Aset DPRD Luwu Timur / Kode Aset: {self.kode_aset}"
        draw = ImageDraw.Draw(qr_img)
        width, height = qr_img.size
        text_width = len(text) * 6
        text_height = 10
        text_x = (width - text_width) // 2
        text_y = height - text_height - 5
        draw.text((text_x, text_y), text, fill='black', font=font)
        return qr_img

    def save(self, *args, **kwargs):
        if not self.kode_aset:
            self.kode_aset = self.generate_kode_aset()

        super(AsetBaru, self).save(*args, **kwargs)

        if not self.qr_code:
            detail_url = reverse('asset_scan_detail', kwargs={'asset_id': self.id})
            absolute_url = self.build_absolute_uri(detail_url)
            qr_img = self.generate_qr_code(absolute_url)
            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")
            self.qr_code.save(f"{self.kode_aset}.png", ContentFile(buffer.getvalue()), save=False)
            super(AsetBaru, self).save(*args, **kwargs)

    def build_absolute_uri(self, detail_url):
        return f"http://127.0.0.1:8000{detail_url}"


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


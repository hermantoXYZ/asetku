# Generated by Django 4.2.13 on 2024-06-23 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_rename_jumlah_pembelian_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pembelian',
            old_name='tanggal_pembelian',
            new_name='tanggal_kontrak',
        ),
    ]

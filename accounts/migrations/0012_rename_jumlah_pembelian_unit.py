# Generated by Django 4.2.13 on 2024-06-23 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_rename_no_invoice_pembelian_no_kontrak'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pembelian',
            old_name='jumlah',
            new_name='unit',
        ),
    ]

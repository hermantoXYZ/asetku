# Generated by Django 4.2.13 on 2024-06-23 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_asetbaru_kondisi_aset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asetbaru',
            name='kondisi_aset',
            field=models.CharField(choices=[('Baik', 'Baik'), ('Rusak', 'Rusak'), ('Rusak Berat', 'Rusak Berat')], default='baik', max_length=12),
        ),
    ]

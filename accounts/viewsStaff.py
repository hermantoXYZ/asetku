from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from . forms import AsetBaruForm, DetailAsetForm, PembelianForm, LampiranForm, ProfileUpdateForm, KategoriForm, PenanggungJawabForm, PosisiAsetForm
from django.contrib.auth.decorators import login_required
from .models import AsetBaru, DetailAset, Pembelian, Lampiran, Kategori, PenanggungJawab, PosisiAsset

from django.db.models import Sum 
from django.template.defaultfilters import floatformat


from django.http import HttpResponse
from tablib import Dataset
from .resources import AsetBaruResource, DetailAsetResource, PembelianResource, LampiranResource, PenanggungJawabResource



def is_staff(user):
    return user.is_authenticated and user.is_staff
@login_required
@user_passes_test(is_staff)
def staff(request):
    total_assets = AsetBaru.objects.all().count()
    total_kategori = Kategori.objects.all().count()
    total_harga_total = Pembelian.objects.aggregate(total_harga=Sum('harga_total'))['total_harga'] or 0
    
    # Format total_harga_total with thousand separators
    total_harga_total_formatted = "{:,}".format(total_harga_total)

    assets = AsetBaru.objects.all().order_by('-id')[:5]
    
    
    context = {
        'total_assets': total_assets,
        'total_kategori': total_kategori,
        'total_harga_total': total_harga_total_formatted,
        'assets': assets,  # Include assets in the context
    }
    return render(request, 'dashboard/staff.html', context)

@login_required
@user_passes_test(is_staff)
def create_aset(request):
    if request.method == 'POST':
        aset_form = AsetBaruForm(request.POST)
        detail_form = DetailAsetForm(request.POST)
        pembelian_form = PembelianForm(request.POST)
        lampiran_form = LampiranForm(request.POST, request.FILES)
        penanggung_jawab_form = PenanggungJawabForm(request.POST)

        
        if (aset_form.is_valid() and detail_form.is_valid() and 
                pembelian_form.is_valid() and lampiran_form.is_valid()):
            aset = aset_form.save()
            detail = detail_form.save(commit=False)
            detail.aset = aset
            detail.save()
            pembelian = pembelian_form.save(commit=False)
            pembelian.aset = aset
            pembelian.save()
            lampiran = lampiran_form.save(commit=False)
            lampiran.aset = aset
            lampiran.save()
            penanggung_jawab = penanggung_jawab_form.save(commit=False)
            penanggung_jawab.aset = aset
            penanggung_jawab.save()
           
            print("All forms are valid and data has been saved. Redirecting to dashboard.")
            return redirect('list_aset')  # Ensure 'dashboard' is the correct URL name for redirection
        else:
            print("Form validation errors found:")
            print("Aset Form Errors:", aset_form.errors)
            print("Detail Form Errors:", detail_form.errors)
            print("Pembelian Form Errors:", pembelian_form.errors)
            print("Lampiran Form Errors:", lampiran_form.errors)
            print("Penanggung Jawab Form Errors:", penanggung_jawab_form.errors)
            
    else:
        aset_form = AsetBaruForm()
        detail_form = DetailAsetForm()
        pembelian_form = PembelianForm()
        lampiran_form = LampiranForm()
        penanggung_jawab_form = PenanggungJawabForm()
  

    context = {
        'aset_form': aset_form,
        'detail_form': detail_form,
        'pembelian_form': pembelian_form,
        'lampiran_form': lampiran_form,
        'penanggung_jawab_form': penanggung_jawab_form
     
    }
    return render(request, 'dashboard/add_assets.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def list_aset(request):
    assets = AsetBaru.objects.all().order_by('-id')
    posisi_aset = PosisiAsset.objects.all()
    lampiran = Lampiran.objects.all()

    context = {
        'assets': assets,
        'posisi_aset': posisi_aset,
        'lampiran': lampiran
    }
    return render(request, 'dashboard/list_assets.html', context)


@user_passes_test(is_staff)
def dashboard_profile(request):
    user = request.user
    return render(request, 'dashboard/profile.html', {'user': user})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'dashboard/profile.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def edit_asset(request, asset_id):
    asset = get_object_or_404(AsetBaru, id=asset_id)

    detail_aset = DetailAset.objects.filter(aset=asset).first()
    pembelian = Pembelian.objects.filter(aset=asset).first()
    lampiran = Lampiran.objects.filter(aset=asset).first()
    penanggung_jawab = PenanggungJawab.objects.filter(aset=asset).first()

    

    if request.method == 'POST':
        aset_form = AsetBaruForm(request.POST, instance=asset)
        detail_form = DetailAsetForm(request.POST, instance=detail_aset)
        pembelian_form = PembelianForm(request.POST, instance=pembelian)
        lampiran_form = LampiranForm(request.POST, request.FILES, instance=lampiran)
        penanggung_jawab_form = PenanggungJawabForm(request.POST, instance=penanggung_jawab)

      

        if (aset_form.is_valid() and detail_form.is_valid() and
                pembelian_form.is_valid() and lampiran_form.is_valid()):
            asset = aset_form.save()
            detail = detail_form.save(commit=False)
            detail.aset = asset
            detail.save()
            pembelian = pembelian_form.save(commit=False)
            pembelian.aset = asset
            pembelian.save()
            lampiran = lampiran_form.save(commit=False)
            lampiran.aset = asset
            lampiran.save()
            penanggung_jawab = penanggung_jawab_form.save(commit=False)
            penanggung_jawab.aset = asset
            penanggung_jawab.save()

            return redirect('list_aset')  # Ganti dengan nama URL halaman yang sesuai setelah berhasil mengedit
    else:
        aset_form = AsetBaruForm(instance=asset)
        detail_form = DetailAsetForm(instance=detail_aset)
        pembelian_form = PembelianForm(instance=pembelian)
        lampiran_form = LampiranForm(instance=lampiran)
        penanggung_jawab_form = PenanggungJawabForm(instance=penanggung_jawab)
       

    context = {
        'aset_form': aset_form,
        'detail_form': detail_form,
        'pembelian_form': pembelian_form,
        'lampiran_form': lampiran_form,
        'penanggung_jawab_form': penanggung_jawab_form,
      
    }
    return render(request, 'dashboard/edit_asset.html', context)

@login_required
@user_passes_test(is_staff)
def delete_asset(request, asset_id):
    asset = get_object_or_404(AsetBaru, id=asset_id)
    
    # Menghapus aset akan secara otomatis menghapus relasi OneToOne terkait jika menggunakan on_delete=models.CASCADE
    asset.delete()
    
    return redirect('list_aset') 
@login_required
@user_passes_test(is_staff)
def tambah_kategori(request):
    if request.method == 'POST':
        form = KategoriForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_kategori')  # Ganti dengan nama URL untuk daftar kategori
    else:
        form = KategoriForm()
    
    context = {
        'form': form,
    }
    return render(request, 'dashboard/tambah_kategori.html', context)

@login_required
@user_passes_test(is_staff)
def tambah_posisi(request):
    if request.method == 'POST':
        form = PosisiAsetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_posisi') 
        
    else:
        form = PosisiAsetForm()
    
    context = {
        'form': form,
    }

    return render(request, 'dashboard/tambah_posisi.html', context)



@login_required
@user_passes_test(is_staff)
def list_kategori(request):
    kategoris = Kategori.objects.all().order_by('-id')
    context = {
        'kategoris': kategoris,
    }
    return render(request, 'dashboard/list_kategori.html', context)

@login_required
@user_passes_test(is_staff)
def list_posisi(request):
    posisis = PosisiAsset.objects.all().order_by('-id')
    context = {
        'posisis': posisis,
    }
    return render(request, 'dashboard/list_posisi.html', context)

@login_required
@user_passes_test(is_staff)
def edit_kategori(request, kategori_id):
    kategori = get_object_or_404(Kategori, id=kategori_id)
    
    if request.method == 'POST':
        form = KategoriForm(request.POST, instance=kategori)
        if form.is_valid():
            form.save()
            return redirect('list_kategori')  # Ganti dengan nama URL untuk daftar kategori setelah edit
    else:
        form = KategoriForm(instance=kategori)
    
    context = {
        'form': form,
    }
    return render(request, 'dashboard/edit_kategori.html', context)


@login_required
@user_passes_test(is_staff)
def edit_lokasi (request, posisi_id):
    posisi = get_object_or_404(PosisiAsset, id=posisi_id)
    
    if request.method == 'POST':
        form = PosisiAsetForm(request.POST, instance=posisi)
        if form.is_valid():
            form.save()
            return redirect('list_posisi')  # Ganti dengan nama URL untuk daftar kategori setelah edit
    else:
        form = PosisiAsetForm(instance=posisi)
    
    context = {
        'form': form,
    }
    return render(request, 'dashboard/edit_posisi.html', context)






@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_kategori(request, kategori_id):
    kategori = get_object_or_404(Kategori, id=kategori_id)
    
    if request.method == 'POST':
        kategori.delete()
        return redirect('list_kategori')
    
    # Redirect jika aksi bukan metode POST (opsional)
    return redirect('list_kategori')



@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_posisi(request, posisi_id):
    posisi = get_object_or_404(PosisiAsset, id=posisi_id)
    
    if request.method == 'POST':
        posisi.delete()
        return redirect('list_posisi')
    
    # Redirect jika aksi bukan metode POST (opsional)
    return redirect('list_posisi')



@login_required
@user_passes_test(is_staff)
def asset_detail(request, asset_id):
    asset = get_object_or_404(AsetBaru, id=asset_id)
    detail_aset = DetailAset.objects.filter(aset=asset).first()
    pembelian = Pembelian.objects.filter(aset=asset).first()
    lampiran = Lampiran.objects.filter(aset=asset)
    penanggung_jawab = PenanggungJawab.objects.filter(aset=asset).first()

    # Format harga_total jika ada
    harga_total_formatted = ""
    if pembelian:
        harga_total_formatted = "{:,.0f}".format(pembelian.harga_total).replace(',', '.')

    context = {
        'asset': asset,
        'detail_aset': detail_aset,
        'pembelian': pembelian,
        'harga_total_formatted': harga_total_formatted,
        'lampiran': lampiran,
        'penanggung_jawab': penanggung_jawab,
    }
    return render(request, 'dashboard/asset_detail.html', context)



def asset_scan_detail(request, asset_id):
    asset = get_object_or_404(AsetBaru, id=asset_id)
    detail_aset = DetailAset.objects.filter(aset=asset).first()
    pembelian = Pembelian.objects.filter(aset=asset).first()
    lampiran = Lampiran.objects.filter(aset=asset)
    penanggung_jawab = PenanggungJawab.objects.filter(aset=asset).first()

    # Format harga_total jika ada
    harga_total_formatted = ""
    if pembelian:
        harga_total_formatted = "{:,.0f}".format(pembelian.harga_total).replace(',', '.')

    context = {
        'asset': asset,
        'detail_aset': detail_aset,
        'pembelian': pembelian,
        'harga_total_formatted': harga_total_formatted,
        'lampiran': lampiran,
        'penanggung_jawab': penanggung_jawab,
    }
    return render(request, 'dashboard/asset_scan_detail.html', context)

@login_required
@user_passes_test(is_staff)
def export_data(request):
    # Initialize resources for each model
    aset_resource = AsetBaruResource()
    detail_resource = DetailAsetResource()
    pembelian_resource = PembelianResource()
    lampiran_resource = LampiranResource()
    penanggung_jawab_resource = PenanggungJawabResource()

    dataset = Dataset()
    dataset.headers = [
        'Nama Aset', 'Kode Aset', 'Kategori', 'Kondisi Aset', 'Posisi Aset',
        'Merk', 'Tipe', 'Produsen', 'No. Seri/Kode Produksi', 'Tahun Produksi', 'Deskripsi',
        'Tanggal Kontrak', 'Toko Distributor', 'No. Kontrak', 'Unit', 'Harga Satuan', 'Harga Total',
        'Nama Lampiran', 'Keterangan Lampiran',
        'Nama Penanggung Jawab', 'Jabatan Penanggung Jawab'
    ]

    # Query data from AsetBaru and related models
    queryset_aset = AsetBaru.objects.all()
    for aset in queryset_aset:
        detail = aset.detail
        pembelian = aset.pembelian.all().first()  # Assuming there's only one pembelian per aset
        lampirans = aset.lampiran.all()
        penanggung_jawabs = aset.penanggung_jawab.all()

        dataset.append([
            aset.nama_aset,
            aset.kode_aset,
            aset.kategori.nama if aset.kategori else '',
            aset.get_kondisi_aset_display(),
            aset.posisi_aset.lokasi if aset.posisi_aset else '',
            detail.merk if detail else '',
            detail.tipe if detail else '',
            detail.produsen if detail else '',
            detail.no_seri_kode_produksi if detail else '',
            detail.tahun_produksi if detail else '',
            detail.deskripsi if detail else '',
            pembelian.tanggal_kontrak if pembelian else '',
            pembelian.toko_distributor if pembelian else '',
            pembelian.no_kontrak if pembelian else '',
            pembelian.unit if pembelian else '',
            pembelian.harga_satuan if pembelian else '',
            pembelian.harga_total if pembelian else '',
            ', '.join([lampiran.foto.name for lampiran in lampirans]) if lampirans else '',
            ', '.join([lampiran.keterangan for lampiran in lampirans]) if lampirans else '',
            ', '.join([pj.nama for pj in penanggung_jawabs]) if penanggung_jawabs else '',
            ', '.join([pj.jabatan for pj in penanggung_jawabs]) if penanggung_jawabs else '',
        ])

    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="combined_data.csv"'
    return response


@login_required
@user_passes_test(is_staff)
def export_posisi_asset(request):
    # Get the filter parameter from the request (e.g., URL query parameter)
    lokasi_filter = request.GET.get('lokasi', None)
    
    dataset = Dataset()
    dataset.headers = [
        'Nama Aset', 'Kode Aset', 'Kategori', 'Kondisi Aset', 'Posisi Aset',
        'Merk', 'Tipe', 'Produsen', 'No. Seri/Kode Produksi', 'Tahun Produksi', 'Deskripsi',
        'Tanggal Kontrak', 'Toko Distributor', 'No. Kontrak', 'Unit', 'Harga Satuan', 'Harga Total',
        'Nama Lampiran', 'Keterangan Lampiran',
        'Nama Penanggung Jawab', 'Jabatan Penanggung Jawab'
    ]

    # Filter data based on the specified 'lokasi'
    if lokasi_filter:
        queryset_posisi = PosisiAsset.objects.filter(lokasi=lokasi_filter)
    else:
        queryset_posisi = PosisiAsset.objects.all()

    # Query data from AsetBaru related to the filtered PosisiAsset
    for posisi in queryset_posisi:
        queryset_aset = AsetBaru.objects.filter(posisi_aset=posisi)
        for aset in queryset_aset:
            detail = aset.detail
            pembelian = aset.pembelian.all().first()  # Assuming there's only one pembelian per aset
            lampirans = aset.lampiran.all()
            penanggung_jawabs = aset.penanggung_jawab.all()

            dataset.append([
                aset.nama_aset,
                aset.kode_aset,
                aset.kategori.nama if aset.kategori else '',
                aset.get_kondisi_aset_display(),
                posisi.lokasi,
                detail.merk if detail else '',
                detail.tipe if detail else '',
                detail.produsen if detail else '',
                detail.no_seri_kode_produksi if detail else '',
                detail.tahun_produksi if detail else '',
                detail.deskripsi if detail else '',
                pembelian.tanggal_kontrak if pembelian else '',
                pembelian.toko_distributor if pembelian else '',
                pembelian.no_kontrak if pembelian else '',
                pembelian.unit if pembelian else '',
                pembelian.harga_satuan if pembelian else '',
                pembelian.harga_total if pembelian else '',
                ', '.join([lampiran.foto.name for lampiran in lampirans]) if lampirans else '',
                ', '.join([lampirans.keterangan for lampirans in lampirans]) if lampirans else '',
                ', '.join([pj.nama for pj in penanggung_jawabs]) if penanggung_jawabs else '',
                ', '.join([pj.jabatan for pj in penanggung_jawabs]) if penanggung_jawabs else '',
            ])

    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="filtered_posisi_asset_data_{lokasi_filter}.csv"'
    return response

@login_required
@user_passes_test(is_staff)
def view_data(request):
    dataset = Dataset()
    dataset.headers = [
        'Nama Aset', 'Kode Aset', 'Kategori', 'Kondisi Aset', 'Posisi Aset',
        'Merk', 'Tipe', 'Produsen', 'No. Seri/Kode Produksi', 'Tahun Produksi', 'Deskripsi',
        'Tanggal Kontrak', 'Toko Distributor', 'No. Kontrak', 'Unit', 'Harga Satuan', 'Harga Total',
        'Nama Lampiran', 'Keterangan Lampiran',
        'Nama Penanggung Jawab', 'Jabatan Penanggung Jawab'
    ]

    # Query data from AsetBaru and related models
    queryset_aset = AsetBaru.objects.all()
    for aset in queryset_aset:
        detail = aset.detail
        pembelian = aset.pembelian.all().first()  # Assuming there's only one pembelian per aset
        lampirans = aset.lampiran.all()
        penanggung_jawabs = aset.penanggung_jawab.all()

        dataset.append([
            aset.nama_aset,
            aset.kode_aset,
            aset.kategori.nama if aset.kategori else '',
            aset.get_kondisi_aset_display(),
            aset.posisi_aset.lokasi if aset.posisi_aset else '',
            detail.merk if detail else '',
            detail.tipe if detail else '',
            detail.produsen if detail else '',
            detail.no_seri_kode_produksi if detail else '',
            detail.tahun_produksi if detail else '',
            detail.deskripsi if detail else '',
            pembelian.tanggal_kontrak if pembelian else '',
            pembelian.toko_distributor if pembelian else '',
            pembelian.no_kontrak if pembelian else '',
            pembelian.unit if pembelian else '',
            pembelian.harga_satuan if pembelian else '',
            pembelian.harga_total if pembelian else '',
            ', '.join([lampiran.foto.name for lampiran in lampirans]) if lampirans else '',
            ', '.join([lampiran.keterangan for lampiran in lampirans]) if lampirans else '',
            ', '.join([pj.nama for pj in penanggung_jawabs]) if penanggung_jawabs else '',
            ', '.join([pj.jabatan for pj in penanggung_jawabs]) if penanggung_jawabs else '',
        ])

    return render(request, 'dashboard/export_data.html', {'dataset': dataset})


@login_required
@user_passes_test(is_staff)
def view_posisi_asset(request):
    # Get the filter parameter from the request (e.g., URL query parameter)
    lokasi_filter = request.GET.get('lokasi', None)
    
    dataset = []
    headers = [
        'Nama Aset', 'Kode Aset', 'Kategori', 'Kondisi Aset', 'Posisi Aset',
        'Merk', 'Tipe', 'Produsen', 'No. Seri/Kode Produksi', 'Tahun Produksi', 'Deskripsi',
        'Tanggal Kontrak', 'Toko Distributor', 'No. Kontrak', 'Unit', 'Harga Satuan', 'Harga Total',
        'Nama Lampiran', 'Keterangan Lampiran',
        'Nama Penanggung Jawab', 'Jabatan Penanggung Jawab'
    ]

    # Filter data based on the specified 'lokasi'
    if lokasi_filter:
        queryset_posisi = PosisiAsset.objects.filter(lokasi=lokasi_filter)
    else:
        queryset_posisi = PosisiAsset.objects.all()

    # Query data from AsetBaru related to the filtered PosisiAsset
    for posisi in queryset_posisi:
        queryset_aset = AsetBaru.objects.filter(posisi_aset=posisi)
        for aset in queryset_aset:
            detail = aset.detail
            pembelian = aset.pembelian.all().first()  # Assuming there's only one pembelian per aset
            lampirans = aset.lampiran.all()
            penanggung_jawabs = aset.penanggung_jawab.all()

            dataset.append([
                aset.nama_aset,
                aset.kode_aset,
                aset.kategori.nama if aset.kategori else '',
                aset.get_kondisi_aset_display(),
                posisi.lokasi,
                detail.merk if detail else '',
                detail.tipe if detail else '',
                detail.produsen if detail else '',
                detail.no_seri_kode_produksi if detail else '',
                detail.tahun_produksi if detail else '',
                detail.deskripsi if detail else '',
                pembelian.tanggal_kontrak if pembelian else '',
                pembelian.toko_distributor if pembelian else '',
                pembelian.no_kontrak if pembelian else '',
                pembelian.unit if pembelian else '',
                pembelian.harga_satuan if pembelian else '',
                pembelian.harga_total if pembelian else '',
                ', '.join([lampiran.foto.name for lampiran in lampirans]) if lampirans else '',
                ', '.join([lampirans.keterangan for lampirans in lampirans]) if lampirans else '',
                ', '.join([pj.nama for pj in penanggung_jawabs]) if penanggung_jawabs else '',
                ', '.join([pj.jabatan for pj in penanggung_jawabs]) if penanggung_jawabs else '',
            ])

    context = {
        'headers': headers,
        'dataset': dataset,
        'lokasi_filter': lokasi_filter,
    }
    return render(request, 'dashboard/export_posisi_asset.html', context)
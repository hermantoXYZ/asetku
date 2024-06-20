from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from . forms import AsetBaruForm, DetailAsetForm, PembelianForm, LampiranForm, ProfileUpdateForm, KategoriForm, PenanggungJawabForm
from django.contrib.auth.decorators import login_required
from .models import AsetBaru, DetailAset, Pembelian, Lampiran, Kategori, PenanggungJawab
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO 
import base64
from PIL import Image, ImageDraw, ImageFont
from django.db.models import Sum 
from django.template.defaultfilters import floatformat
from django.shortcuts import reverse
from urllib.parse import urlparse


def generate_qr_code(data, kode_aset):
    
    # Initialize QRCode instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Generate QR code image
    qr_img = qr.make_image(fill='black', back_color='white')
    
    # Convert QR code image to PIL Image
    qr_pil_img = qr_img.convert('RGB')
    width, height = qr_pil_img.size
    
    # Load a font
    font = ImageFont.load_default()
    
    # Define text to be added below QR code
    text = f"Aset DPRD Luwu Timur / Kode Aset: {kode_aset}"
    
    # Estimate text size and position (adjust as needed)
    text_width = len(text) * 6  # Adjust based on font and text characteristics
    text_height = 10  # Adjust based on font size and text characteristics
    text_x = (width - text_width) // 2  # Center the text horizontally
    text_y = height - text_height - 5  # 5 pixels margin from the bottom
    
    # Create a drawing context
    draw = ImageDraw.Draw(qr_pil_img)
    
    # Add text to the image
    draw.text((text_x, text_y), text, fill='black', font=font)
    
    return qr_pil_img

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

    assets = AsetBaru.objects.all().order_by('-id')
    
    for asset in assets:
    

        detail_url = request.build_absolute_uri(reverse('asset_scan_detail', kwargs={'asset_id': asset.id}))
        qr_data = f"Kode Aset: {asset.kode_aset}\nLink: {detail_url}"
        
        # Generate QR code image with additional text
        qr_img = generate_qr_code(qr_data, asset.kode_aset)
        
        # Convert image to base64 string
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        qr_img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        asset.qr_code_img = qr_img_str  # Save base64 string for template
    
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


# @user_passes_test(is_staff)
# def list_aset(request):
#     assets = AsetBaru.objects.all()
#     for asset in assets:
#         qr_data = f"Nama Aset: {asset.nama_aset}\nKode Aset: {asset.kode_aset}\nKategori: {asset.kategori}"
#         qr_img = generate_qr_code(qr_data)
#         buffer = BytesIO()
#         qr_img.save(buffer, format="PNG")
#         qr_img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
#         asset.qr_code_img = qr_img_str  # Simpan string base64 sementara untuk template
#     context = {
#         'assets': assets,
#     }
#     return render(request, 'dashboard/list_assets.html', context)
@login_required
@user_passes_test(is_staff)
def list_aset(request):
    assets = AsetBaru.objects.all().order_by('-id')
    for asset in assets:
        

        detail_url = request.build_absolute_uri(reverse('asset_scan_detail', kwargs={'asset_id': asset.id}))

        parsed_url = urlparse(detail_url)
        url_to_display = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

        # qr_data = f"Kode Aset: {asset.kode_aset}\nLink: {detail_url}"
        
        # Generate QR code image with additional text
        qr_img = generate_qr_code(url_to_display, asset.kode_aset)
        
        # Convert image to base64 string
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        qr_img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        asset.qr_code_img = qr_img_str  # Simpan string base64 sementara untuk template
    
    context = {
        'assets': assets,
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
def list_kategori(request):
    kategoris = Kategori.objects.all().order_by('-id')
    context = {
        'kategoris': kategoris,
    }
    return render(request, 'dashboard/list_kategori.html', context)

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
@user_passes_test(lambda u: u.is_staff)
def delete_kategori(request, kategori_id):
    kategori = get_object_or_404(Kategori, id=kategori_id)
    
    if request.method == 'POST':
        kategori.delete()
        return redirect('list_kategori')
    
    # Redirect jika aksi bukan metode POST (opsional)
    return redirect('list_kategori')

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
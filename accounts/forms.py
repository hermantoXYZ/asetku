from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Kategori, AsetBaru, DetailAset, Pembelian, Lampiran, PenanggungJawab
from num2words import num2words

class CurrencyInput(forms.TextInput):
    def __init__(self, attrs=None):
        final_attrs = {'class': 'currency'}
        if attrs is not None:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2', 'is_user')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data["phone_number"]
        user.is_pelanggan = self.cleaned_data["is_user"]
        if commit:
            user.save()
        return user
    
    def clean_is_pelanggan(self):
        is_pelanggan = self.cleaned_data.get("is_user")
        if not is_pelanggan:
            raise forms.ValidationError("You must agree to our Terms...")
        return is_pelanggan

    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email has been registered...")
        return email

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'image']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Tambahkan validasi email di sini jika diperlukan
        return email



class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()


class PasswordResetConfirmForm(forms.Form):
    verification_code = forms.CharField(max_length=6)
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'image']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Tambahkan validasi email di sini jika diperlukan
        return email


class AsetBaruForm(forms.ModelForm):
    class Meta:
        model = AsetBaru
        fields = ['nama_aset', 'kode_aset', 'kategori']

class DetailAsetForm(forms.ModelForm):
    class Meta:
        model = DetailAset
        fields = ['merk', 'tipe', 'produsen', 'no_seri_kode_produksi', 'tahun_produksi', 'deskripsi']



class PembelianForm(forms.ModelForm):
    tanggal_pembelian = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    harga_total_text = forms.CharField(label='Harga Total Terbilang', required=False)  # Tambahkan field untuk menyimpan teks harga total
    harga_total = forms.FloatField(label='Harga Total', min_value=0) 
    class Meta:
        model = Pembelian
        fields = ['tanggal_pembelian', 'toko_distributor', 'no_invoice', 'jumlah', 'harga_satuan', 'harga_total']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inisialisasi nilai teks harga_total jika ada instance yang sudah ada
        if self.instance and self.instance.harga_total:
            self.initial['harga_total_text'] = num2words(self.instance.harga_total, lang='id')

    def clean(self):
        cleaned_data = super().clean()
        harga_total = cleaned_data.get('harga_total')
        if harga_total:
            cleaned_data['harga_total_text'] = num2words(harga_total, lang='id')  # Konversi harga_total ke teks
        return cleaned_data
    

class LampiranForm(forms.ModelForm):
    class Meta:
        model = Lampiran
        fields = ['foto', 'keterangan']

# class PenyusutanForm(forms.ModelForm):
#     class Meta:
#         model = Penyusutan
#         fields = ['umur_ekonomis']

class PenanggungJawabForm(forms.ModelForm):
    class Meta:
        model = PenanggungJawab
        fields= ['nama', 'jabatan']

class KategoriForm(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = ['nama']
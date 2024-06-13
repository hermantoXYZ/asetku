from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

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
    

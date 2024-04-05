from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Role, Product


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    phone_number = forms.CharField(label="Phone Number", max_length=20, required=False)
    role = forms.ModelChoiceField(queryset=Role.objects.all(), label="Role", required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'email', 'password1', 'phone_number', 'role')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['productname', 'description', 'price', 'image']
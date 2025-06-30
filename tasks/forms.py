from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from .models import Task
from .models import Unavailability

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'is_admin')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'is_admin')

class UnavailabilityForm(forms.ModelForm):
    class Meta:
        model = Unavailability
        fields = ['start_date', 'end_date', 'reason']  # Kullanıcının girmesi gereken alanlar

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['document']  # Assuming 'document' is the FileField in your Task model

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

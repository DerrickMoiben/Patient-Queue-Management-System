from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient, Visit, Triage


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )

    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'role',
            'password1',
            'password2',
        ]
        
        
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    
    
from django import forms
from django.forms import TextInput, Select, DateInput, EmailInput

class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'date_of_birth': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': Select(attrs={'class': 'form-select'}),
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
        }
        
class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        exclude = ["created_by", "queue_number", "status", "current_department", "visit_date"]
        fields = '__all__'
        widgets = {
            'patient': Select(attrs={'class': 'form-select'}),
            'current_department': Select(attrs={'class': 'form-select'}),
            'status': Select(attrs={'class': 'form-select'}),
        }

class TriageForm(forms.ModelForm):
    class Meta:
        model = Triage
        exclude = ["visit"]
        fields = '__all__'
        widgets = {
            'blood_pressure': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blood pressure'}),
            'heart_rate': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter heart rate'}),
            'temperature': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter temperature'}),
            'respiratory_rate': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter respiratory rate'}),
            'oxygen_saturation': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter oxygen saturation'}),
            'weight': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter weight'}),
            'height': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter height'}),
        }
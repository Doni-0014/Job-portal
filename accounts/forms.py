from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css = 'form-control'
            if field_name == 'role':
                css = 'form-select'
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing + ' ' + css).strip()
        self.fields['username'].widget.attrs.setdefault('placeholder', 'Username')
        self.fields['email'].widget.attrs.setdefault('placeholder', 'Email')
        self.fields['password1'].widget.attrs.setdefault('placeholder', 'Password')
        self.fields['password2'].widget.attrs.setdefault('placeholder', 'Confirm Password')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing + ' form-control').strip()
        self.fields['username'].widget.attrs.setdefault('placeholder', 'Username')
        self.fields['password'].widget.attrs.setdefault('placeholder', 'Password')

from allauth.socialaccount.forms import SignupForm
# from .models import User
from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm as RegisterForm
from django.contrib.auth import password_validation

User = get_user_model()

class MyCustomSocialSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(MyCustomSocialSignupForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["readonly"] = True
        # self.fields["email"].widget.attrs["disabled"] = True
        self.fields["email"].label_attr = {'class': 'white-label'}

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use. Please Login with password")
        return email

    def save(self, request):
        user = super(MyCustomSocialSignupForm, self).save(request)
        user.username = self.cleaned_data["username"]
        user.save()
        return user


from django import forms

class RegistrationForm(ModelForm):
    confirmpassword = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'input_field',
            'id': 'cpassword_field',
            'placeholder': 'Confirm password',
            'style': 'background-color: #C1CAE3; color: black;',
            'autocomplete': 'off',
            'required': True,
            'minlength': 8,
        })
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password', ]
        
    username = forms.CharField(
        label='Username (unique)',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input_field',
            'id': 'username_field',
            'placeholder': 'Username',
            'style': 'background-color: #C1CAE3; color: black;',
            'autocomplete': 'off',
            'required': True,
            'minlength': 3
        })
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'input_field',
            'id': 'email_field',
            'placeholder': 'name@mail.com',
            'style': 'background-color: #C1CAE3; color: black;',
            'autocomplete': 'off',
            'required': True,
        })
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'input_field',
            'id': 'password_field',
            'placeholder': 'Password',
            'style': 'background-color: #C1CAE3; color: black;',
            'autocomplete': 'off',
            'required': True,
            'minlength': 8,
        })
    )
    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     if password:
    #         password_validation.validate_password(password, self.instance)
    #     return password

    

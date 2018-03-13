from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#Login form
class SigninForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                #raise forms.ValidationError("Cet utilisateur n'existe pas")
                raise forms.ValidationError("Nom d'utilisateur ou mot de passe incorrect")
            if not user.check_password(password):
                raise forms.ValidationError("Mot de passe incorrect")
            if not user.is_active:
                raise forms.ValidationError("Ce compte n'est pas actif")
        return super(SigninForm, self).clean(*args, **kwargs)

#Register form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        #Le model user
        model = User
        #Liste des champs que l'on veut pour le formulaire d'inscription
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        if not password1 == password2:
            raise forms.ValidationError("Les deux mots de passe ne matchent pas.")
        count = User.objects.filter(email=email).count()
        if email and count > 0:
            raise forms.ValidationError(u"Cet email existe déjà")
        return email

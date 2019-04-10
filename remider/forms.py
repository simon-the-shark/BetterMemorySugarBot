from django import forms

class GetSecretForm(forms.Form):
    apisecret = forms.CharField(required=True, widget=forms.PasswordInput, label='SECRET_KEY')

class FileUploudForm(forms.Form):
    file = forms.FileField()
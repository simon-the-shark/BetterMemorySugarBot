from django import forms

class GetSecretForm(forms.Form):
    apisecret = forms.CharField(required=True)
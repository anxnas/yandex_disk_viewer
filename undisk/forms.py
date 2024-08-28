from django import forms

class PublicLinkForm(forms.Form):
    public_key = forms.CharField(label='Public key', max_length=255)
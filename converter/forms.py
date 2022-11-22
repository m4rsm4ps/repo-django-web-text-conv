from django import forms


class ConverterForm(forms.Form):
    to_convert = forms.CharField(label='Text to convert', widget=forms.Textarea)

from django import forms

class CountryForm(forms.Form):
    country = forms.ChoiceField()
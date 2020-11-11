from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class CompanyForm(forms.Form):
    company_name = forms.CharField()
    country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    company_email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()



# from django.forms import ModelForm, SelectMultiple
from django import forms
from dal import autocomplete
from core.models import Field_Metadata, Schedule_Part_Metadata, FilingFiling, Organization

class OrganizationForm(forms.ModelForm):
    # queryset = FilingFiling.objects.distinct('ein')
    # queryset = Organization.objects.all()
    # taxpayer_name = forms.ModelChoiceField(
    #     queryset=Organization.objects.filter(id__lte=1000),
    #     widget=autocomplete.ModelSelect2(url='org-autocomplete')
    # )

    class Meta:
        model = Organization
        fields = ('taxpayer_name',)
        widgets = {
            'taxpayer_name': autocomplete.ListSelect2(url='org-autocomplete')
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['taxpayer_name'].choices = [(x.ein, x.taxpayer_name) for x in FilingFiling.objects.distinct('ein')]

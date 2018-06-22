# from django.forms import ModelForm, SelectMultiple
from django import forms
from django.forms.formsets import BaseFormSet
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
            'taxpayer_name': autocomplete.Select2Multiple(url='org-autocomplete', attrs={'class': 'form-control'})
        }
        labels = {
            'taxpayer_name': ('Nonprofit Names'),
        }


class FieldsForm(forms.Form):
    field_names = forms.ModelMultipleChoiceField(queryset=Field_Metadata.objects.none(), widget=forms.CheckboxSelectMultiple)

    # def __init__(self, parent_sked_part_id, *args, **kwargs):
    #     super(FieldsForm, self).__init__()
    #     self.fields['fields'].queryset = Field_Metadata.objects.filter(parent_sked_part=parent_sked_part_id)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['taxpayer_name'].choices = [(x.ein, x.taxpayer_name) for x in FilingFiling.objects.distinct('ein')]


class FieldsFormSet(BaseFormSet):

    def __init__(self, *args, **kwargs):
        parent_sked_part_ids = kwargs.pop('parent_sked_part_ids')
        super(FieldsFormSet, self).__init__(*args, **kwargs)
      #after call to super, self.forms is populated with the forms

        #associating first form with first applicant, second form with second applicant and so o
        for index, form in enumerate(self.forms):
            parent_sked_part_id = parent_sked_part_ids[index]
            form.fields['field_names'].queryset = Field_Metadata.objects.filter(parent_sked_part_id=parent_sked_part_id)
            sked_part = Schedule_Part_Metadata.objects.get(id=parent_sked_part_id)
            form.name = sked_part.part_name
            form.sked_name = sked_part.parent_sked.name


class OrganizationTypeForm(forms.Form):
    choices = (
        (1, '990'),
        (2, '990EZ'),
        (3, '990PF')
    )

    return_type = forms.ChoiceField(choices=choices)


    class Meta:
        widgets = {
            'return_type': forms.CheckboxInput( attrs={'class': 'form-control'})
        }


class SchedulePartForm(forms.Form):
    def __init__(self, *args, **kwargs):
        form_type = kwargs.pop('form_type')  # this may come through as a text field
        if form_type:
            schedule_parts = forms.ModelMultipleChoiceField(queryset=Schedule_Part_Metadata.objects.filter())

# from django.forms import ModelForm, SelectMultiple
from django import forms
from django.forms.formsets import BaseFormSet
from django.db.models import Q
from dal import autocomplete
from core.models import Field_Metadata, Schedule_Part_Metadata, FilingFiling, Organization, Schedule_Metadata, Fiscal_Year

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


class OrganizationSingleForm(forms.ModelForm):
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
            'taxpayer_name': autocomplete.Select2(url='org-autocomplete', attrs={'class': 'form-control'})
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

    return_type = forms.ChoiceField(
        choices=choices,
        help_text="Is this a private foundation (990PF)? Are the organization's gross receipts less than $200,000 and total assets less than $500,000 (990EZ)? Are its gross receipts worth at least $200,000 and total assets at least $500,000 (990)?",
        widget=forms.Select(
            attrs={
                'class': 'custom-select form-control'
            }
        )
    )


    # class Meta:
    #     widgets = {
    #         'return_type': forms.CheckboxInput(attrs={'class': 'custom-select form-control'})
    #     }


class SchedulePartsForm(forms.Form):
    schedule_parts = forms.ModelMultipleChoiceField(
        queryset=Field_Metadata.objects.none(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'form-control'
            }
        )
    )

    # def __init__(self, *args, **kwargs):
    #     return_type = kwargs.pop('return_type')  # this may come through as a text field
    #     super(SchedulePartsForm, self).__init__(*args, **kwargs)
    #     if return_type == '1':
    #         queryset = Schedule_Part_Metadata.objects.exclude(Q(part_key__istartswith='pf') | Q(part_key__istartswith='ez'))
    #     elif return_type == '2':
    #         queryset = Schedule_Part_Metadata.objects.filter(part_key__istartswith='ez')
    #     else:
    #         queryset = Schedule_Part_Metadata.objects.filter(part_key__istartswith='pf')
    #
    #     schedule_parts = forms.ModelMultipleChoiceField(queryset=queryset)


# this is a formset that represents the Schedule (grouping Schedule Parts underneath)
class SchedulePartsFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        # return_type = kwargs.pop('return_type')  # this may come through as a text field
        parent_sked_ids = kwargs.pop('parent_sked_ids')
        super(SchedulePartsFormSet, self).__init__(*args, **kwargs)
        #
        # if return_type == '1':
        #     schedule_queryset = Schedule_Part_Metadata.objects.exclude(Q(part_key__istartswith='pf') | Q(part_key__istartswith='ez'))
        # elif return_type == '2':
        #     schedule_queryset = Schedule_Part_Metadata.objects.filter(part_key__istartswith='ez')
        # else:
        #     schedule_queryset = Schedule_Part_Metadata.objects.filter(part_key__istartswith='pf')


        for index, form in enumerate(self.forms):
            parent_sked_id = parent_sked_ids[index]
            form.fields['schedule_parts'].queryset = Schedule_Part_Metadata.objects.filter(parent_sked_id=parent_sked_id)
            parent_sked = Schedule_Metadata.objects.get(id=parent_sked_id)
            form.parent_sked_name = parent_sked.name

        # schedule_parts = forms.ModelMultipleChoiceField(queryset=queryset)


class FiscalYearForm(forms.Form):
    # qs = FilingFiling.objects.values_list('tax_period', flat=True).distinct()
    qs = Fiscal_Year.objects.values_list('fiscal_year', flat=True).distinct()
    yr_map = {}

    for fiscal_year in qs:
        if fiscal_year not in yr_map.keys():
            yr_map[fiscal_year] = fiscal_year


    choices = tuple([
        tuple([yr, yr_key]) for yr_key, yr in yr_map.items()
    ])

    choices = sorted(choices, key=lambda x: x[1])

    # print(choices)

    year = forms.MultipleChoiceField(
        choices=choices,
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control'
            }
        )
    )

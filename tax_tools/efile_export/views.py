import json
import csv
from django.shortcuts import render
from dal import autocomplete
from core.models import Organization, Schedule_Part_Metadata, FilingFiling, Schedule_Metadata
from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.forms import formset_factory
from django.views import View
from django.db.models import Q
from efile_export.generate_report import generate_report, get_return_type_label
from efile_export.forms import (OrganizationForm, FieldsForm, FieldsFormSet,
                                OrganizationTypeForm, SchedulePartsForm,
                                SchedulePartsFormSet, OrganizationSingleForm,
                                FiscalYearForm)

# Create your views here.
# def home(request):
#     return render(request, 'efile_export/test.html', {'form': form})

SESSION_KEYS = {
    'org_id': 'org_id',
    'year': 'year',
    'return_type': 'return_type',
    'schedule_parts': 'schedule_parts'
}
# class ReportSuccess(TemplateView):
#     template_name = 'efile_export/success.html'


def stream_report(request):
    archive = generate_report(request)
    response = HttpResponse(archive, content_type='application/x-zip-compressed')
    response['Content-Disposition'] = "attachment; filename=\"990export.zip\""


    # writer = csv.writer(response)

    # writer.writerows(generate_report(request))  commented for commit

    # writer.writerow(['ha HA', 'foo', 'bar'])
    # writer.writerow(['ha HO', 'baz', 'spam'])

    return response


def report_success(request):
    # check for all keys in session
    session_keys = SESSION_KEYS.values()
    for key in session_keys:
        if key not in request.session.keys():
            raise Http404
        else:

            return render(request, 'efile_export/success.html')
            # use session keys to build queryset
            # generate CSV (separate fnct)
            # stream CSV (separate fnct)
            # render page


class Home(TemplateView):
    template_name = 'efile_export/home.html'


# def org_form(request):
#     if request.method == 'POST':
#         print(request.POST)
#         print(OrganizationForm(request.POST))
#
#     print('queryin')
#     form = OrganizationForm()
#     print('renderin')
#
#     return render(request, 'efile_export/test.html', {'form': form})

class SimpleFormBase(View):
    '''Abstracted base class for simple form views'''
    page_title = None
    template_path = None
    action_url = None
    description_text = None
    next_page_url = None
    session_key = None
    cleaned_data_key = None

    def generate_form(self, request):
        raise NotImplementedError

    def generate_context(self, request):
        return {
            'page_title': self.page_title,
            'action_url': self.action_url,
            'description_text': self.description_text,
            'form': self.generate_form(request)
        }

    def get(self, request):
        context = self.generate_context(request)
        return render(request, self.template_path, context)

    def post(self, request):
        print(request.POST)
        context = self.generate_context(request)
        form = context['form']
        print(request.session.keys())
        # print(form.errors)
        if form.is_valid():
            request.session[self.session_key] = form.cleaned_data[self.cleaned_data_key]
            request.session.save()  # not sure if this is necessary
            return HttpResponseRedirect(reverse_lazy(self.next_page_url))
        else:
            print('FUCK')
            return render(request, self.template_path, context)


class OrgForm(SimpleFormBase):
    page_title = 'Organization Select'
    template_path = 'efile_export/simple_form.html'
    action_url = 'org-form'
    description_text = '''Begin to type the name of a nonprofit you'd like to
        include in your report and it should appear below. Select as many
        nonprofits you'd like to include, although please note you will only
        be able to include organizations that file the type of form you
        specified previously. <em>Note:</em> The typeahead box below may initially take some time to load.'''
    next_page_url = 'sked-parts-form'
    session_key = 'org_id'
    cleaned_data_key = 'taxpayer_name'

    def generate_form(self, request):
        initial = {'org_id': request.session.get('org_id', None)}
        form = OrganizationForm(request.POST or None, initial=initial)

        return form

    def get(self, request):
        if 'return_type' not in request.session.keys() or 'year' not in request.session.keys():
            raise Http404("Please start this form from the beginning")
        return super().get(request)


class FYForm(SimpleFormBase):
    page_title = 'Fiscal Years'
    template_path = 'efile_export/simple_form.html'
    action_url = 'fy-form'
    description_text = "Select as many fiscal years as you'd like to include in your efile report from the list below."
    next_page_url = 'org-form'
    session_key = 'year'
    cleaned_data_key = 'year'

    def generate_form(self, request):
        form = FiscalYearForm(request.POST or None)
        # print(form)

        return form


class OrgTypeForm(SimpleFormBase):
    page_title = 'Organization Type'
    template_path = 'efile_export/type_form.html'
    action_url = 'type-form'
    description_text = "Select the organization type below. Not sure which 990 your organizations file? Look it up in the search box at the bottom of this page."
    next_page_url = 'fy-form'
    session_key = 'return_type'
    cleaned_data_key = session_key

    def generate_context(self, request):
        forms = self.generate_form(request)
        return {
            'page_title': self.page_title,
            'action_url': self.action_url,
            'description_text': self.description_text,
            'form': forms['type'],
            'autocomp_form': forms['autocomp_form']
        }

    def generate_form(self, request):
        form = OrganizationTypeForm(request.POST or None)
        autocomp_form = OrganizationSingleForm(request.POST or None)
        return {'type': form, 'autocomp_form': autocomp_form}


# def org_form(request):
#     initial = {'org_id': request.session.get('org_id', None)}
#     form = OrganizationForm(request.POST or None, initial=initial)
#     context = {
#         'action_url': 'org-form',
#         'page_title': 'choooooose your orgs',
#         'form': form,
#         'description_text': 'placeholder text tktktktktktkt tk tkk tk tk tk ktkttktk ktk tkt ktkt ktk ktktkk tk'
#     }
#     if request.method == 'POST':
#         print(request.POST)
#         if form.is_valid():
#             print('valid!!!')
#             request.session['org_id'] = form.cleaned_data['taxpayer_name']
#             request.session.save()
#             return HttpResponseRedirect(reverse_lazy('field-form'))
#     return render(request, 'efile_export/org_form.html', context)

    # return redirect()


class SkedPartsForm(SimpleFormBase):
    page_title = 'Schedule Parts'
    template_path = 'efile_export/sked_parts_form.html'
    action_url = 'sked-parts-form'
    description_text = 'tktktk'
    next_page_url = 'report-success'
    session_key = 'schedule_parts'
    cleaned_data_key = session_key

    def generate_form(self, request):
        return_type = request.session['return_type']
        if return_type == '1':
            base_form = Schedule_Metadata.objects.get(name='IRS990')
            # parent_sked_ids = Schedule_Part_Metadata.objects.exclude(Q(part_key__istartswith='pf') | Q(part_key__istartswith='ez') | Q(part_key='returnheader990x_part_i')).values_list('parent_sked_id', flat=True).distinct()
        elif return_type == '2':
            base_form = Schedule_Metadata.objects.get(name='IRS990EZ')
            # parent_sked_ids = Schedule_Part_Metadata.objects.filter(part_key__istartswith='ez').exclude(part_key='returnheader990x_part_i').values_list('parent_sked_id', flat=True).distinct()
        else:
            base_form = Schedule_Metadata.objects.get(name='IRS990PF')
            # parent_sked_ids = Schedule_Part_Metadata.objects.filter(part_key__istartswith='pf').exclude(part_key='returnheader990x_part_i').values_list('parent_sked_id', flat=True).distinct()

        parent_sked_ids = [base_form.id] + list(base_form.schedules.all().values_list('id', flat=True).distinct())

        SchedulePartsFormSetFactory = formset_factory(SchedulePartsForm, formset=SchedulePartsFormSet, extra=len(parent_sked_ids))
        schedule_parts_form_set = SchedulePartsFormSetFactory(request.POST or None, request.FILES or None, parent_sked_ids=parent_sked_ids)

        return schedule_parts_form_set

    def post(self, request):
        print(request.POST)
        context = self.generate_context(request)
        form = context['form']
        # print(form.errors)
        if form.is_valid():  #  formset
            sked_part_ids = []
            for key, value in request.POST.items():
                if 'field_names' in key:
                    sked_part_ids += request.POST.getlist(key)
                    # print(value)
            # form.clean()
            header_id = Schedule_Part_Metadata.objects.get(part_key='returnheader990x_part_i').id
            sked_part_ids.append(header_id)
            print(sked_part_ids)
            # print(form.cleaned_data)
            request.session[self.session_key] = sked_part_ids
            request.session['report_form_completed'] = True
            request.session.save()  # not sure if this is necessary
            print(request.session.keys())
            return HttpResponseRedirect(reverse_lazy(self.next_page_url))
        else:
            return render(request, self.template_path, context)


def field_form(request):
    sked_part_ids = Schedule_Part_Metadata.objects.values_list('id', flat=True).distinct()
    # formset = formset_factory(FieldsForm) # FieldsForm(request.POST or None)
    # fields_formset = formset()
    # print(request.session['org_id'])
    FieldsFormSetFactory = formset_factory(FieldsForm, formset=FieldsFormSet, extra=len(sked_part_ids))
    if request.method == 'POST':
        print(request.POST)
        print(request.session)
        fields_form_set = FieldsFormSetFactory(request.POST, request.FILES, parent_sked_part_ids=sked_part_ids)
        if fields_form_set.is_valid():
            # print(form)  # generate report object here
            return HttpResponseRedirect(reverse_lazy('export-home'))
    else:
        fields_form_set = FieldsFormSetFactory(parent_sked_part_ids=sked_part_ids)
    return render(request, 'efile_export/field_form.html', {'formset': fields_form_set})


class OrgNameAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        return_type_coded = self.request.session['return_type']
        fiscal_years = self.request.session['year']
        # print(fiscal_years)
        # print(return_type_coded)
        return_type_list = get_return_type_label(return_type_coded)
        q_filters = Q()
        for fy in fiscal_years:
            q_filters = q_filters | Q(fiscal_year__fiscal_year=fy)
        qs = Organization.objects.filter(q_filters, return_type__in=return_type_list)

        if self.q:
            return qs.filter(taxpayer_name__istartswith=self.q)
        else:
            return qs


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def get_org_return_type(request):
    if request.method == 'POST':
        print(request.POST)
        try:
            ein = request.POST['taxpayer_name']
        except (IndexError, KeyError):
            print('ah fuc ', request.POST)

        print(ein)

    data = {}

    try:
        return_type = FilingFiling.objects.filter(ein=ein).order_by('-sub_date')[0].return_type
        data = {'return_type': return_type}
    except FilingFiling.DoesNotExist:
        print ('oh NO')

    return HttpResponse(json.dumps(data), content_type="application/json")

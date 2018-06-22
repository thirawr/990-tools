from django.shortcuts import render
from dal import autocomplete
from efile_export.forms import OrganizationForm, FieldsForm, FieldsFormSet, OrganizationTypeForm
from core.models import Organization, Schedule_Part_Metadata
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.forms import formset_factory
from django.views import View

# Create your views here.
# def home(request):
#     return render(request, 'efile_export/test.html', {'form': form})


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
        form = self.generate_form(request)
        print(form.errors)
        if form.is_valid():  # this is broken: should probably implement post on each subclass. need to be specific about session.
            # request.session['eins'] = form.cleaned_data['taxpayer_name']
            # request.session.save()  # not sure if this is necessary
            return HttpResponseRedirect(reverse_lazy(self.next_page_url))
        else:
            return render(request, self.template_path, context)


class OrgForm(SimpleFormBase):
    page_title = 'Organization Select'
    template_path = 'efile_export/simple_form.html'
    action_url = 'org-form'
    description_text = '''Begin to type the name of a nonprofit you'd like to
        include in your report and it should appear below. Select as many
        nonprofits you'd like to include, although please note you will only
        be able to include organizations that file the type of form you
        specified previously.'''
    next_page_url = 'field-form'

    def generate_form(self, request):
        initial = {'eins': request.session.get('eins', None)}
        form = OrganizationForm(request.POST or None, initial=initial)

        return form


class OrgTypeForm(SimpleFormBase):
    page_title = 'Organization Type'
    template_path = 'efile_export/simple_form.html'
    action_url = 'type-form'
    description_text = 'tktktk'
    next_page_url = 'org-form'

    def generate_form(self, request):
        form = OrganizationTypeForm(request.POST or None)
        return form


def org_form(request):
    initial = {'eins': request.session.get('eins', None)}
    form = OrganizationForm(request.POST or None, initial=initial)
    context = {
        'action_url': 'org-form',
        'page_title': 'choooooose your orgs',
        'form': form,
        'description_text': 'placeholder text tktktktktktkt tk tkk tk tk tk ktkttktk ktk tkt ktkt ktk ktktkk tk'
    }
    if request.method == 'POST':
        print(request.POST)
        if form.is_valid():
            print('valid!!!')
            request.session['eins'] = form.cleaned_data['taxpayer_name']
            request.session.save()
            return HttpResponseRedirect(reverse_lazy('field-form'))
    return render(request, 'efile_export/org_form.html', context)

    # return redirect()


def field_form(request):
    sked_part_ids = Schedule_Part_Metadata.objects.values_list('id', flat=True).distinct()
    # formset = formset_factory(FieldsForm) # FieldsForm(request.POST or None)
    # fields_formset = formset()
    print(request.session['eins'])
    FieldsFormSetFactory = formset_factory(FieldsForm, formset=FieldsFormSet, extra=len(sked_part_ids))
    if request.method == 'POST':
        print(request.POST)
        print(request.session)
        fields_form_set = FieldsFormSetFactory(request.POST, request.FILES, parent_sked_part_ids=sked_part_ids)
        if fields_form_set.is_valid():
            # print(form)  # generate report object here
            return HttpResponseRedirect(reverse_lazy('export_home'))
    else:
        fields_form_set = FieldsFormSetFactory(parent_sked_part_ids=sked_part_ids)
    return render(request, 'efile_export/field_form.html', {'formset': fields_form_set})


class OrgNameAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Organization.objects.all()

        if self.q:
            qs = qs.filter(taxpayer_name__istartswith=self.q)

        return qs

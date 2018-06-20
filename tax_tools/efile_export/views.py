from django.shortcuts import render
from dal import autocomplete
from efile_export.forms import OrganizationForm
from core.models import Organization
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

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


def org_form(request):
    initial = {'eins': request.session.get('eins', None)}
    form = OrganizationForm(request.POST or None, initial=initial)
    if request.method == 'POST':
        print(request.POST)
        if form.is_valid():
            request.session['eins'] = form.cleaned_data['taxpayer_name']
            return HttpResponseRedirect(reverse_lazy('field-form'))
    return render(request, 'efile_export/org_form.html', {'form': form})

    # return redirect()


def field_form(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.session)
        return redirect('export_home')


class OrgForm(FormView):
    template_name = 'efile_export/org_form.html'
    form_class = OrganizationForm
    success_url = Home.as_view()

    def form_valid(self, form):
        return HttpResponse('yoooooooooo')



# class UpdateView(generic.UpdateView):
#     model = Organization
#     form_class = OrganizationForm
#     template_name = 'efile_export/test.html'
#     success_url = reverse_lazy('export_home')
#
#     def get_object(self):
#         return Organization.objects.first()


class OrgNameAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Organization.objects.all()

        if self.q:
            qs = qs.filter(taxpayer_name__istartswith=self.q)

        return qs

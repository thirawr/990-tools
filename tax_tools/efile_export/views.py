from django.shortcuts import render
from dal import autocomplete
from efile_export.forms import OrganizationForm
from core.models import Organization
from django.views import generic
from django.urls import reverse_lazy

# Create your views here.
def home(request):
    if request.method == 'POST':
        print(request.POST)
        print(OrganizationForm(request.POST))

    print('queryin')
    form = OrganizationForm()
    print('renderin')

    return render(request, 'efile_export/test.html', {'form': form})


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

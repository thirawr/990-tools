from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from core.models import Schedule_Part_Metadata, FilingFiling, Schedule_Metadata, Field_Metadata

# Create your views here.
class SkedPartList(ListView):
    # browse this page to advance to the SkedPartList
    # maybe use those expanding cards to group sked parts under sked here
    model = Schedule_Metadata


class FieldsList(ListView):
    # this view will take a URL parameter indicating the sked part for which it should show fields
    # display variables in table format
    def get_queryset(self):
        self.sked_part = get_object_or_404(Schedule_Part_Metadata, id=self.kwargs['sked_part_id'])
        return Field_Metadata.objects.filter(parent_sked_part=self.sked_part)

class FieldDetail(DetailView):
    # show varaible metadata
    # optional?
    # maybe show some extra fields not on the VariableList table
    pass

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from core.models import Schedule_Part_Metadata, FilingFiling, Schedule_Metadata, Field_Metadata
import logging

log = logging.getLogger(__name__)

# Create your views here.
class DocListViewBase(ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav_app'] = 'docs'
        return context


class DocDetailViewBase(DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav_app'] = 'docs'
        return context


class SkedPartList(DocListViewBase):
    # browse this page to advance to the SkedPartList
    # maybe use those expanding cards to group sked parts under sked here
    model = Schedule_Metadata

    def get_queryset(self):
        if 'sked_id' in self.kwargs.keys():
            return Schedule_Metadata.objects.filter(id=self.kwargs['sked_id'])
        else:
            return super().get_queryset()
# class IndividualSkedPartList(DocListViewBase):
#     model = Schedule_Metadata
#
#     def get_queryset(self):
#         return Schedule_Metadata.objects.filter(id=self.request.sked_id)


class FieldsList(DocListViewBase):
    # this view will take a URL parameter indicating the sked part for which it should show fields
    # display variables in table format
    def get_queryset(self):
        self.sked_part = get_object_or_404(Schedule_Part_Metadata, id=self.kwargs['sked_part_id'])
        return Field_Metadata.objects.filter(parent_sked_part=self.sked_part).order_by('ordering')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sked_part_name'] = self.sked_part.part_name
        context['sked_name'] = self.sked_part.parent_sked.name
        return context


class FieldDetail(DocDetailViewBase):
    # show varaible metadata
    # optional?
    # maybe show some extra fields not on the VariableList table
    model = Field_Metadata

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get associated forms - if this is not a schedule this will just be its parent sked
        context['associated_forms'] = self.object.parent_sked.associated_forms.all()
        return context

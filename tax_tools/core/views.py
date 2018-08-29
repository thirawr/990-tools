from django.shortcuts import render
from django.views.generic import ListView, DetailView
from core.models import Schedule_Part_Metadata, FilingFiling, Schedule_Metadata

# Create your views here.
class SkedPartList(ListView):
    # browse this page to advance to the SkedPartList
    # maybe use those expanding cards to group sked parts under sked here
    model = Schedule_Metadata


class SkedPartDetail(ListView):
    # this view will take a URL parameter indicating the sked part for which it should show fields
    # display variables in table format
    pass


class VariableDetail(DetailView):
    # show varaible metadata
    # optional?
    # maybe show some extra fields not on the VariableList table
    pass

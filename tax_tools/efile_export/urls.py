"""tax_tools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from efile_export.views import Home, OrgNameAutocomplete, org_form, field_form, OrgForm, OrgTypeForm, SkedPartsForm, FYForm, get_org_return_type, report_success, stream_report

urlpatterns = [
    path('', Home.as_view(), name='export-home'),
    path('org-form', OrgForm.as_view(), name='org-form'),
    path('field-form', field_form, name='field-form'),
    path('type-form', OrgTypeForm.as_view(), name='type-form'),
    path('sked-parts-form', SkedPartsForm.as_view(), name='sked-parts-form'),
    path('fy-form', FYForm.as_view(), name='fy-form'),
    path('success', report_success, name='report-success'),
    path('stream_report', stream_report, name='stream_report'),
    path('org-autocomplete/', OrgNameAutocomplete.as_view(), name='org-autocomplete'),
    path('org-type-lookup/', get_org_return_type, name='get-org-type')
]

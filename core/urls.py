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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from efile_export import urls as export_urls
from core.views import SkedPartList, FieldDetail, FieldsList

urlpatterns = [
    path('schedules/', SkedPartList.as_view(), name='reference-skeds'),
    path('schedules/<int:sked_id>', SkedPartList.as_view(), name='reference-skeds'),
    path('sked-part/<int:sked_part_id>/', FieldsList.as_view(), name='reference-sked-part'),
    path('field/<int:pk>/', FieldDetail.as_view(), name='reference-field-detail'),
]

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
from efile_export.views import OrgSearch

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('efile_export.urls')),
    path('export/', include('efile_export.urls')),
    path('reference/', include('core.urls')),
    # path('search/', include('haystack.urls')),
    path('search/', OrgSearch.as_view(), name='org_search_view'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path(r'__debug__/', include(debug_toolbar.urls))] + urlpatterns

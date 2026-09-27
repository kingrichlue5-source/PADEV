"""
URL configuration for lacd_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.sitemaps import (
    ProgramSitemap, ProjectSitemap, NewsUpdateSitemap,
    SuccessStorySitemap, PublicationSitemap, ProcurementSitemap, CareerSitemap,
    HeroSlideSitemap, ProgramStructureSitemap,
)

sitemaps = {
    'programs': ProgramSitemap(),
    'projects': ProjectSitemap(),
    'news': NewsUpdateSitemap(),
    'stories': SuccessStorySitemap(),
    'publications': PublicationSitemap(),
    'procurements': ProcurementSitemap(),
    'careers': CareerSitemap(),
    'hero_slides': HeroSlideSitemap(),
    'program_structure': ProgramStructureSitemap(),
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django-sitemaps'),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


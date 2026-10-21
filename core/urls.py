from django.urls import path
from django.views.generic.base import RedirectView
from .views import (
    HomeView, TeamView, ProgramListView, ProgramDetailView,
    ProjectListView, ProjectDetailView, ProcurementListView,
    CareerListView, PublicationListView, ContactView,
    NewsUpdateDetailView, NewsUpdateListView, SuccessStoryDetailView,
    PublicationDetailView, ProcurementDetailView, CareerDetailView,
    HeroSlideDetailView, ProgramStructureDetailView, AboutView,
)

app_name = 'core'

urlpatterns = [
    # Main Navigation Content Routes
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('team/', TeamView.as_view(), name='team'),
    path('contact/', ContactView.as_view(), name='contact'),
    
    # Structural Content Feeds
    path('programmes/', ProgramListView.as_view(), name='program_list'),
    path('programmes/<slug:slug>/', ProgramDetailView.as_view(), name='program_detail'),
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('news/', NewsUpdateListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', NewsUpdateDetailView.as_view(), name='news_detail'),
    path('stories/<slug:slug>/', SuccessStoryDetailView.as_view(), name='story_detail'),
    path('publications/', PublicationListView.as_view(), name='publication_list'),
    path('publications/<slug:slug>/', PublicationDetailView.as_view(), name='publication_detail'),
    path('procurement/', ProcurementListView.as_view(), name='procurement_list'),
    path('procurement/<slug:slug>/', ProcurementDetailView.as_view(), name='procurement_detail'),
    path('careers/', CareerListView.as_view(), name='career_list'),
    path('careers/<slug:slug>/', CareerDetailView.as_view(), name='career_detail'),
    
    # Internal Slide Elements
    path('hero/<slug:slug>/', HeroSlideDetailView.as_view(), name='hero_detail'),
    path('program-structure/<slug:slug>/', ProgramStructureDetailView.as_view(), name='program_structure_detail'),

    # Hard-Coded 301 Permanent Redirects for Old WordPress Links (SEO Protection)
    path('about-us/', RedirectView.as_view(url='/about/', permanent=True)),
    path('new-views/', RedirectView.as_view(url='/news/', permanent=True)),
    path('gallery/', RedirectView.as_view(url='/projects/', permanent=True)),
]

from django.urls import path
from .views import (
    HomeView, TeamView, ProgramListView, ProgramDetailView,
    ProjectListView, ProjectDetailView, ProcurementListView,
    CareerListView, PublicationListView, ContactView,
    NewsUpdateDetailView, SuccessStoryDetailView,
    PublicationDetailView, ProcurementDetailView, CareerDetailView,
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('team/', TeamView.as_view(), name='team'),
    path('programmes/', ProgramListView.as_view(), name='program_list'),
    path('programmes/<slug:slug>/', ProgramDetailView.as_view(), name='program_detail'),
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('news/<slug:slug>/', NewsUpdateDetailView.as_view(), name='news_detail'),
    path('stories/<slug:slug>/', SuccessStoryDetailView.as_view(), name='story_detail'),
    path('publications/', PublicationListView.as_view(), name='publication_list'),
    path('publications/<slug:slug>/', PublicationDetailView.as_view(), name='publication_detail'),
    path('procurement/', ProcurementListView.as_view(), name='procurement_list'),
    path('procurement/<slug:slug>/', ProcurementDetailView.as_view(), name='procurement_detail'),
    path('careers/', CareerListView.as_view(), name='career_list'),
    path('careers/<slug:slug>/', CareerDetailView.as_view(), name='career_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
]

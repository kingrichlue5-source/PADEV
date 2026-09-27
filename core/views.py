from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, FormView
from hitcount.views import HitCountDetailView
from django.contrib import messages
from django.db.models import Q
from .models import (
    Program, Project, NewsUpdate, SuccessStory, TeamMember, Client,
    Publication, ProcurementOpportunity, Career, ContactSubmission,
    HeroSlide, SiteSetting, ProgramStructure, LIBERIA_COUNTIES,
)

CATEGORY_TITLES = {
    'founder': 'Founders',
    'board': 'Board of Directors',
    'management': 'Management Team',
}
CATEGORY_ORDER = ['founder', 'board', 'management']


def _team_payload(members, start):
    return [
        {
            'index': start + i,
            'name': m.full_name,
            'position': m.position,
            'role': m.get_role_category_display(),
            'bio': m.bio,
            'photo': m.photo.url if m.photo else '',
        }
        for i, m in enumerate(members)
    ]


def _structure_grid_cols(count):
    """Tailwind grid column classes for the floating Program Structure cards."""
    if count <= 1:
        return 'lg:grid-cols-1'
    if count == 2:
        return 'sm:grid-cols-2 lg:grid-cols-2'
    if count in (3, 5, 6):
        # 3 columns: 5 cards wrap as 3 + 2 instead of leaving a lonely 5th card
        return 'sm:grid-cols-2 lg:grid-cols-3'
    return 'sm:grid-cols-2 lg:grid-cols-4'


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero_slides'] = HeroSlide.objects.filter(is_active=True).order_by('order', 'created_at')

        # Floating "Program Structure" cards below the hero
        structure_cards = list(
            ProgramStructure.objects.filter(is_active=True).order_by('order', 'created_at')
        )
        context['program_structure'] = structure_cards
        context['program_structure_cols'] = _structure_grid_cols(len(structure_cards))

        # "Our Core Programmes" grid — every published programme (up to 6),
        # with featured ones listed first if more than six exist
        context['programs'] = Program.objects.order_by('-is_featured', '-created_at')[:6]
        # "Active County Projects" — projects still running, featured ones first,
        # falling back to featured projects if nothing is currently running
        active_projects = list(
            Project.objects.filter(status='ongoing').order_by('-is_featured', '-created_at')[:3]
        )
        context['projects'] = active_projects or list(Project.objects.filter(is_featured=True)[:3])
        context['news_list'] = NewsUpdate.objects.all()[:3]
        context['success_stories'] = SuccessStory.objects.filter(is_featured=True)[:3]
        context['clients'] = Client.objects.filter(is_active=True)

        # Statistics for impact counter
        agency = SiteSetting.get_instance()
        context['total_projects'] = Project.objects.count()
        context['total_communities'] = 100
        context['total_beehives'] = 190
        context['total_counties'] = 15
        context['agency_acronym'] = agency.agency_acronym
        return context

    def post(self, request, *args, **kwargs):
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', 'General Inquiry')
        message_text = request.POST.get('message')

        if full_name and email and message_text:
            ContactSubmission.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                subject=subject,
                message=message_text
            )
            messages.success(request, "Thank you! Your message has been received by PADEV. We will get back to you shortly.")
            return redirect('core:home')
        else:
            messages.error(request, "Please fill in all required fields.")
            return self.get(request, *args, **kwargs)


class AboutView(TemplateView):
    template_name = 'about.html'


class TeamView(TemplateView):
    template_name = 'team.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_members = list(TeamMember.objects.filter(is_active=True))
        groups = []
        flat = []
        for key in CATEGORY_ORDER:
            members = sorted(
                [m for m in all_members if m.role_category == key],
                key=lambda m: (m.order, m.full_name),
            )
            if not members:
                continue
            group_data = _team_payload(members, len(flat))
            groups.append({'title': CATEGORY_TITLES[key], 'members': group_data})
            flat.extend(group_data)
        context['team_groups'] = groups
        context['team_data'] = flat
        return context


class ProgramListView(ListView):
    model = Program
    template_name = 'program_list.html'
    context_object_name = 'programs'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.GET.get('status')
        county_filter = self.request.GET.get('county')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if county_filter:
            queryset = queryset.filter(county=county_filter)
        return queryset


class ProgramDetailView(HitCountDetailView):
    model = Program
    template_name = 'program_detail.html'
    context_object_name = 'program'
    count_hit = True


class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'
    context_object_name = 'projects'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['counties'] = LIBERIA_COUNTIES
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.GET.get('status')
        county_filter = self.request.GET.get('county')
        search_query = self.request.GET.get('q')

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if county_filter:
            queryset = queryset.filter(county=county_filter)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(short_description__icontains=search_query) |
                Q(contractor__icontains=search_query)
            )
        return queryset


class ProjectDetailView(HitCountDetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'
    count_hit = True


class ProcurementListView(ListView):
    model = ProcurementOpportunity
    template_name = 'procurement_list.html'
    context_object_name = 'procurements'

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.GET.get('status')
        category_filter = self.request.GET.get('category')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if category_filter:
            queryset = queryset.filter(category=category_filter)
        return queryset


class CareerListView(ListView):
    model = Career
    template_name = 'career_list.html'
    context_object_name = 'careers'

    def get_queryset(self):
        return Career.objects.filter(is_active=True)


class PublicationListView(ListView):
    model = Publication
    template_name = 'publication_list.html'
    context_object_name = 'publications'
    paginate_by = 8


class NewsUpdateDetailView(HitCountDetailView):
    model = NewsUpdate
    template_name = 'news_detail.html'
    context_object_name = 'news'
    count_hit = True


class SuccessStoryDetailView(HitCountDetailView):
    model = SuccessStory
    template_name = 'story_detail.html'
    context_object_name = 'story'
    count_hit = True


class PublicationDetailView(HitCountDetailView):
    model = Publication
    template_name = 'publication_detail.html'
    context_object_name = 'publication'
    count_hit = True


class ProcurementDetailView(HitCountDetailView):
    model = ProcurementOpportunity
    template_name = 'procurement_detail.html'
    context_object_name = 'procurement'
    count_hit = True


class CareerDetailView(HitCountDetailView):
    model = Career
    template_name = 'career_detail.html'
    context_object_name = 'career'
    count_hit = True


class HeroSlideDetailView(HitCountDetailView):
    """Full 'Read More' article for a homepage hero slide."""
    model = HeroSlide
    template_name = 'hero_detail.html'
    context_object_name = 'slide'
    count_hit = True

    def get_queryset(self):
        return HeroSlide.objects.filter(is_active=True)


class ProgramStructureDetailView(HitCountDetailView):
    """Full article for a homepage Program Structure card."""
    model = ProgramStructure
    template_name = 'program_structure_detail.html'
    context_object_name = 'card'
    count_hit = True

    def get_queryset(self):
        return ProgramStructure.objects.filter(is_active=True)


class ContactView(TemplateView):
    template_name = 'contact.html'

    def post(self, request, *args, **kwargs):
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', 'General Contact')
        message_text = request.POST.get('message')

        if full_name and email and message_text:
            ContactSubmission.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                subject=subject,
                message=message_text
            )
            messages.success(request, "Your message has been submitted successfully!")
            return redirect('core:contact')
        else:
            messages.error(request, "Please ensure all mandatory fields are completed.")
            return render(request, self.template_name)

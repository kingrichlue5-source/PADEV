from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from unfold.decorators import display
from .models import (
    Program, Project, NewsUpdate, SuccessStory, TeamMember, Client,
    Publication, ProcurementOpportunity, Career, ContactSubmission,
    SiteSetting, NavigationMenu, HeroSlide, ProgramStructure,
)
from hitcount.models import HitCount, Hit, BlacklistIP, BlacklistUserAgent

# ─── Unregister default User/Group and re-register with Unfold ───

admin.site.unregister(User)
admin.site.unregister(Group)

# ─── Unregister default hitcount admins (plain ModelAdmin) ───

admin.site.unregister(HitCount)
admin.site.unregister(Hit)
admin.site.unregister(BlacklistIP)
admin.site.unregister(BlacklistUserAgent)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


# ─── Site Settings (Singleton) ───

@admin.register(SiteSetting)
class SiteSettingAdmin(ModelAdmin):
    list_display = ('site_name', 'agency_acronym', 'contact_email', 'contact_phone')
    fieldsets = (
        ('Branding', {'fields': ('site_name', 'agency_acronym', 'logo')}),
        ('Hero Section', {
            'fields': ('hero_background_image', 'hero_text'),
            'description': 'Background image behind the homepage hero, and the "Hero Text" headline. Start a new line for a line break; wrap words in ** to show them in the gold gradient.',
        }),
        ('Program Structure Section', {
            'fields': ('program_structure_heading', 'program_structure_intro'),
            'description': 'Heading and introduction shown above the Program Structure cards on the homepage. The cards themselves are managed under "Program Structure".',
        }),
        ('Contact & Social', {'fields': ('contact_email', 'contact_phone', 'address', 'social_links')}),
    )
    compressed_fields = True

    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ─── Navigation Menus ───

class NavigationMenuInline(TabularInline):
    model = NavigationMenu
    fk_name = 'parent'
    extra = 1
    fields = ('title', 'url', 'order', 'badge_text', 'is_active')


@admin.register(NavigationMenu)
class NavigationMenuAdmin(ModelAdmin):
    list_display = ('title', 'parent', 'order', 'display_badge', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('title', 'url', 'badge_text')
    list_editable = ('order', 'is_active')
    inlines = [NavigationMenuInline]
    fieldsets = (
        ('Navigation', {'fields': ('title', 'url', 'parent', 'order', 'badge_text', 'is_active')}),
    )

    @display(description="Badge", label=True)
    def display_badge(self, instance):
        if instance.badge_text:
            return instance.badge_text
        return None


# ─── Hero Slides ───

@admin.register(HeroSlide)
class HeroSlideAdmin(ModelAdmin):
    list_display = ('title', 'badge_text', 'order', 'display_status')
    list_filter = ('is_active',)
    search_fields = ('title', 'description', 'badge_text', 'detail_content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order',)
    fieldsets = (
        ('Slide Content', {
            'fields': ('badge_text', 'title', 'slug', 'description', 'slide_image'),
        }),
        ('Read More Page', {
            'fields': ('detail_content',),
            'description': 'The full article opened by the "Read More" button on the homepage. Start a new paragraph on a new line.',
        }),
        ('Settings', {
            'fields': ('order', 'is_active'),
        }),
    )

    @display(
        description="Status",
        label={
            "Active": "success",
            "Inactive": "danger",
        },
    )
    def display_status(self, instance):
        return "Active" if instance.is_active else "Inactive"


# ─── Program Structure (homepage floating cards) ───

@admin.register(ProgramStructure)
class ProgramStructureAdmin(ModelAdmin):
    list_display = ('title', 'display_theme', 'icon_class', 'order', 'is_active')
    list_filter = ('theme', 'is_active')
    search_fields = ('title', 'description', 'detail_content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order', 'is_active')
    compressed_fields = True
    fieldsets = (
        ('Card Content', {
            'fields': ('title', 'slug', 'description', 'icon_class'),
        }),
        ('Details Page', {
            'fields': ('detail_content',),
            'description': 'The full article opened when the card title is clicked on the homepage. Start a new paragraph on a new line.',
        }),
        ('Appearance', {
            'fields': ('theme',),
        }),
        ('Settings', {
            'fields': ('order', 'is_active'),
        }),
    )

    @display(
        description="Theme",
        label={
            "Green": "success",
            "Gold": "warning",
            "Navy": "info",
            "Rose": "danger",
        },
    )
    def display_theme(self, instance):
        return instance.get_theme_display()


# ─── Programs ───

@admin.register(Program)
class ProgramAdmin(ModelAdmin):
    list_display = ('title', 'display_status', 'county', 'budget', 'is_featured', 'created_at')
    list_filter = ('status', 'county', 'is_featured')
    search_fields = ('title', 'short_description', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured',)
    list_filter_submit = True
    compressed_fields = True

    @display(
        description="Status",
        label={
            "Active": "success",
            "Upcoming": "info",
            "Completed": "warning",
        },
    )
    def display_status(self, instance):
        return instance.get_status_display()


# ─── Projects ───

@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ('title', 'county', 'display_status', 'display_progress', 'budget', 'is_featured')
    list_filter = ('status', 'county', 'is_featured', 'program')
    search_fields = ('title', 'short_description', 'contractor', 'location_details')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured',)
    list_filter_submit = True
    compressed_fields = True

    @display(
        description="Status",
        label={
            "Planning": "info",
            "Ongoing / In Progress": "warning",
            "Completed": "success",
            "On Hold": "danger",
        },
    )
    def display_status(self, instance):
        return instance.get_status_display()

    @display(description="Progress")
    def display_progress(self, instance):
        pct = instance.progress_percentage
        if pct >= 75:
            color = "#22c55e"
        elif pct >= 40:
            color = "#eab308"
        else:
            color = "#ef4444"
        return format_html(
            '<div style="width:100px;background:#e5e7eb;border-radius:6px;overflow:hidden;">'
            '<div style="width:{}%;background:{};height:8px;border-radius:6px;"></div>'
            '</div>'
            '<span style="font-size:0.75rem;color:#6b7280;">{}%</span>',
            pct, color, pct,
        )


# ─── News & Updates ───

@admin.register(NewsUpdate)
class NewsUpdateAdmin(ModelAdmin):
    list_display = ('title', 'display_category', 'author', 'published_date', 'is_featured')
    list_filter = ('category', 'is_featured', 'published_date')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured',)
    list_filter_submit = True

    @display(
        description="Category",
        label={
            "Press Release": "success",
            "Agency Announcement": "info",
            "Field Progress Update": "warning",
            "Official Event": "info",
        },
    )
    def display_category(self, instance):
        return instance.get_category_display()


# ─── Success Stories ───

@admin.register(SuccessStory)
class SuccessStoryAdmin(ModelAdmin):
    list_display = ('title', 'beneficiary_name', 'county', 'is_featured', 'created_at')
    list_filter = ('county', 'is_featured')
    search_fields = ('title', 'beneficiary_name', 'quote', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured',)


# ─── Team Members ───

@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ('full_name', 'position', 'display_role', 'order', 'is_active')
    list_filter = ('role_category', 'is_active')
    search_fields = ('full_name', 'position', 'bio')
    list_editable = ('order', 'is_active')

    @display(
        description="Role",
        label=True,
    )
    def display_role(self, instance):
        return instance.get_role_category_display()


# ─── Clients & Partners ───

@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    search_fields = ('name',)
    list_editable = ('order', 'is_active')


# ─── Publications ───

@admin.register(Publication)
class PublicationAdmin(ModelAdmin):
    list_display = ('title', 'display_category', 'publication_date', 'download_count')
    list_filter = ('category', 'publication_date')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

    @display(
        description="Category",
        label=True,
    )
    def display_category(self, instance):
        return instance.get_category_display()


# ─── Procurement Opportunities ───

@admin.register(ProcurementOpportunity)
class ProcurementOpportunityAdmin(ModelAdmin):
    list_display = ('reference_number', 'title', 'category', 'display_status', 'opening_date', 'closing_deadline')
    list_filter = ('status', 'category')
    search_fields = ('reference_number', 'title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_filter_submit = True

    @display(
        description="Status",
        label={
            "Open for Submission": "success",
            "Under Evaluation": "warning",
            "Awarded": "info",
            "Closed": "danger",
        },
    )
    def display_status(self, instance):
        return instance.get_status_display()


# ─── Careers ───

@admin.register(Career)
class CareerAdmin(ModelAdmin):
    list_display = ('job_title', 'department', 'job_type', 'application_deadline', 'display_status')
    list_filter = ('job_type', 'is_active', 'department')
    search_fields = ('job_title', 'department', 'description', 'requirements')
    prepopulated_fields = {'slug': ('job_title',)}
    list_filter_submit = True

    @display(
        description="Status",
        label={
            "Open": "success",
            "Closed": "danger",
        },
    )
    def display_status(self, instance):
        return "Open" if instance.is_active else "Closed"


# ─── Contact Submissions (Read-only) ───

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'submitted_at', 'is_read')
    list_filter = ('is_read', 'submitted_at')
    search_fields = ('full_name', 'email', 'subject', 'message')
    readonly_fields = ('full_name', 'email', 'phone', 'subject', 'message', 'submitted_at')
    list_editable = ('is_read',)

    @display(
        description="Read",
        label={
            "Read": "success",
            "Unread": "danger",
        },
    )
    def display_read_status(self, instance):
        return "Read" if instance.is_read else "Unread"


# ─── Hitcount (re-registered with Unfold) ───

@admin.register(HitCount)
class HitCountAdmin(ModelAdmin):
    list_display = ('content_object', 'hits', 'modified')
    fields = ('hits',)
    readonly_fields = ('hits',)
    search_fields = ('content_object',)
    list_filter = ('modified',)
    compressed_fields = True

    def has_add_permission(self, request):
        return False


@admin.register(Hit)
class HitAdmin(ModelAdmin):
    list_display = ('created', 'user', 'ip', 'user_agent', 'hitcount')
    search_fields = ('ip', 'user_agent')
    date_hierarchy = 'created'
    readonly_fields = ('created', 'ip', 'session', 'user_agent', 'user', 'hitcount')
    compressed_fields = True

    def has_add_permission(self, request):
        return False


@admin.register(BlacklistIP)
class BlacklistIPAdmin(ModelAdmin):
    list_display = ('ip',)
    search_fields = ('ip',)


@admin.register(BlacklistUserAgent)
class BlacklistUserAgentAdmin(ModelAdmin):
    list_display = ('user_agent',)
    search_fields = ('user_agent',)

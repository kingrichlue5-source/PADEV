from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=255, default='Partners in Development (PADEV)')
    agency_acronym = models.CharField(max_length=50, default='PADEV')
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    contact_email = models.EmailField(default='info@padev.org')
    contact_phone = models.CharField(max_length=50, default='+231 088 651 8396')
    address = models.CharField(max_length=255, default='Sophie Community, Opposite HILA School, Congo Town, Monrovia, Liberia')
    social_links = models.JSONField(default=dict, blank=True)
    hero_background_image = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Optional background image for the hero section on the homepage")
    hero_text = models.TextField(
        default="Start Your Community's\n**Beautiful & Bright** Future.",
        help_text=(
            "Homepage headline. Start a new line for a line break; wrap words in ** "
            "to show them in the gold gradient. Leave blank to hide the headline."
        ),
    )
    program_structure_heading = models.CharField(
        max_length=120,
        default='Program Structure',
        help_text="Heading shown above the Program Structure cards on the homepage",
    )
    program_structure_intro = models.TextField(
        blank=True,
        default='Driven by specialized expertise, Partners in Development delivers impactful solutions across four core areas: Forest Governance, Livelihood & Enterprise Development, Strategic Communication, and Stakeholder Engagement.',
        help_text="Introduction shown under the heading on the homepage. Leave blank to hide it.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        obj, _ = cls.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Partners in Development (PADEV)',
                'agency_acronym': 'PADEV',
                'contact_email': 'info@padev.org',
                'contact_phone': '+231 088 651 8396',
                'address': 'Sophie Community, Opposite HILA School, Congo Town, Monrovia, Liberia',
                'hero_background_image': None,
            },
        )
        return obj

    def __str__(self):
        return self.site_name


class NavigationMenu(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255, blank=True, default='#')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    badge_text = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Navigation Menu'
        verbose_name_plural = 'Navigation Menus'

    def __str__(self):
        return self.title


class HeroSlide(models.Model):
    badge_text = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    description = models.TextField(blank=True)
    detail_content = models.TextField(blank=True, help_text="Full article shown on this slide's Read More page (new paragraphs start on a new line)")
    slide_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Hero Slide'
        verbose_name_plural = 'Hero Slides'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:hero_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class ProgramStructure(models.Model):
    """A card in the floating 'Program Structure' row overlapping the homepage hero."""

    THEME_CHOICES = [
        ('green', 'Green'),
        ('gold', 'Gold'),
        ('navy', 'Navy'),
        ('rose', 'Rose'),
    ]

    # Tailwind classes applied to the icon box for each colour theme
    THEME_STYLES = {
        'green': 'bg-emerald-50 text-lacd-green group-hover:bg-lacd-green group-hover:text-lacd-gold',
        'gold': 'bg-amber-50 text-amber-600 group-hover:bg-lacd-gold group-hover:text-lacd-navy',
        'navy': 'bg-sky-50 text-sky-600 group-hover:bg-lacd-navy group-hover:text-lacd-gold',
        'rose': 'bg-rose-50 text-rose-600 group-hover:bg-rose-600 group-hover:text-white',
    }

    title = models.CharField(max_length=200, help_text="Card heading e.g. Community Forest Governance")
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    description = models.TextField(max_length=300, help_text="Short copy shown under the heading")
    detail_content = models.TextField(blank=True, help_text="Full article shown when the card title is clicked (new paragraphs start on a new line)")
    icon_class = models.CharField(max_length=100, default='ri-leaf-line', help_text="Remix icon class name e.g. ri-tree-line")
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='green')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Program Structure Card'
        verbose_name_plural = 'Program Structure'

    @property
    def icon_box_classes(self):
        return self.THEME_STYLES.get(self.theme, self.THEME_STYLES['green'])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:program_structure_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


# List of 15 Counties in Liberia for choice fields
LIBERIA_COUNTIES = [
    ('bomi', 'Bomi'),
    ('bong', 'Bong'),
    ('gbarpolu', 'Gbarpolu'),
    ('grand_bassa', 'Grand Bassa'),
    ('grand_cape_mount', 'Grand Cape Mount'),
    ('grand_gedeh', 'Grand Gedeh'),
    ('grand_kru', 'Grand Kru'),
    ('lofa', 'Lofa'),
    ('margibi', 'Margibi'),
    ('maryland', 'Maryland'),
    ('montserrado', 'Montserrado'),
    ('nimba', 'Nimba'),
    ('river_cess', 'River Cess'),
    ('river_gee', 'River Gee'),
    ('sinoe', 'Sinoe'),
    ('national', 'Nationwide / Multiple Counties'),
]

class Program(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    icon_class = models.CharField(max_length=100, default='ri-community-line', help_text="Remix/FontAwesome icon class name e.g. ri-road-ster-line")
    short_description = models.TextField(max_length=500, help_text="Brief snippet for cards")
    description = models.TextField(help_text="Detailed program description")
    cover_image = models.ImageField(upload_to='programs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    county = models.CharField(max_length=50, choices=LIBERIA_COUNTIES, default='national')
    budget = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. $2,500,000 USD")
    target_beneficiaries = models.CharField(max_length=200, blank=True, null=True, help_text="e.g. 50,000 Farmers & Youth")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description (max 160 chars)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Development Program'
        verbose_name_plural = 'Development Programs'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:program_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Project(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('ongoing', 'Ongoing / In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    short_description = models.TextField(max_length=500)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    county = models.CharField(max_length=50, choices=LIBERIA_COUNTIES, default='montserrado')
    location_details = models.CharField(max_length=255, blank=True, help_text="District, town or community name")
    progress_percentage = models.PositiveIntegerField(default=0, help_text="0 to 100 percent")
    budget = models.CharField(max_length=100, blank=True, help_text="Allocated budget e.g. $450,000 USD")
    contractor = models.CharField(max_length=255, blank=True, help_text="Lead contractor or execution agency")
    donor = models.CharField(max_length=255, blank=True, help_text="Funding organisation e.g. GEF, USAID, Sweden Embassy")
    implementing_agency = models.CharField(max_length=255, blank=True, help_text="Lead sector or executing agency e.g. Forestry Development Authority (FDA)")
    partners = models.TextField(blank=True, help_text="Partner organisations, one per line")
    report_link = models.URLField(max_length=500, blank=True, help_text="Public link to the project report or factsheet")
    start_date = models.DateField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description (max 160 chars)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'County Project'
        verbose_name_plural = 'County Projects'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:project_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.title} ({self.get_county_display()})"


class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('management', 'Management Team'),
        ('founder', 'Founders & Board'),
        ('board', 'Board of Directors'),
    ]

    full_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200, help_text="e.g. Team Leader, Deputy Team Leader, Cofounder")
    role_category = models.CharField(max_length=20, choices=ROLE_CHOICES, default='management')
    bio = models.TextField(blank=True, help_text="Short biography shown in the team popup")
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    email = models.EmailField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['role_category', 'order', 'full_name']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return self.full_name


class Client(models.Model):
    name = models.CharField(max_length=150, help_text="Organization name e.g. USAID")
    logo = models.ImageField(upload_to='clients/', blank=True, null=True)
    website = models.URLField(blank=True, help_text="Optional official website link")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Client / Partner'
        verbose_name_plural = 'Clients & Partners'

    def __str__(self):
        return self.name


class NewsUpdate(models.Model):
    CATEGORY_CHOICES = [
        ('press_release', 'Press Release'),
        ('announcement', 'Agency Announcement'),
        ('field_update', 'Field Progress Update'),
        ('event', 'Official Event'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    author = models.CharField(max_length=100, default='PADEV Communications Team')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='press_release')
    excerpt = models.TextField(max_length=400, help_text="Short abstract for news feeds")
    content = models.TextField(help_text="Full news article content")
    featured_image = models.ImageField(upload_to='news/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description (max 160 chars)")
    published_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = 'News & Update'
        verbose_name_plural = 'News & Updates'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:news_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class SuccessStory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    beneficiary_name = models.CharField(max_length=150, help_text="Community name, farmer group or individual")
    county = models.CharField(max_length=50, choices=LIBERIA_COUNTIES, default='bong')
    quote = models.TextField(max_length=300, help_text="Key quote from beneficiary")
    content = models.TextField(help_text="Detailed story background and impact")
    featured_image = models.ImageField(upload_to='stories/', blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description (max 160 chars)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Success Story'
        verbose_name_plural = 'Success Stories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:story_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.title} - {self.beneficiary_name}"


class Publication(models.Model):
    CATEGORY_CHOICES = [
        ('annual_report', 'Annual Report'),
        ('strategic_plan', 'Strategic Plan'),
        ('policy_document', 'Policy & Framework'),
        ('procurement_report', 'Procurement & Financial Audit'),
        ('research', 'Research & Case Study'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='annual_report')
    description = models.TextField(max_length=500, blank=True)
    pdf_file = models.FileField(upload_to='publications/pdf/', help_text="Upload PDF document")
    cover_image = models.ImageField(upload_to='publications/covers/', blank=True, null=True)
    file_size = models.CharField(max_length=50, blank=True, help_text="e.g. 4.2 MB")
    publication_date = models.DateField()
    download_count = models.PositiveIntegerField(default=0)
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description (max 160 chars)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-publication_date']
        verbose_name = 'Publication & Report'
        verbose_name_plural = 'Publications & Reports'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:publication_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"


class ProcurementOpportunity(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open for Submission'),
        ('under_evaluation', 'Under Evaluation'),
        ('awarded', 'Awarded'),
        ('closed', 'Closed'),
    ]
    CATEGORY_CHOICES = [
        ('rfq', 'Request for Quotation (RFQ)'),
        ('rfp', 'Request for Proposal (RFP)'),
        ('eoi', 'Expression of Interest (EOI)'),
        ('ncb', 'National Competitive Bidding'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    reference_number = models.CharField(max_length=100, unique=True, help_text="e.g. PADEV/RFQ/2026/004")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='rfq')
    description = models.TextField(help_text="Scope of work and tender requirements summary")
    tender_document = models.FileField(upload_to='tenders/', help_text="PDF document upload")
    opening_date = models.DateField()
    closing_deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    contact_email = models.EmailField(default='procurement@padev.org')
    submission_location = models.CharField(max_length=255, default='PADEV HQ Procurement Office, Sophie Community, Congo Town, Monrovia')
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description (max 160 chars)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-opening_date']
        verbose_name = 'Procurement Opportunity'
        verbose_name_plural = 'Procurement Opportunities'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:procurement_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.reference_number}: {self.title}"


class Career(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full-Time'),
        ('contract', 'Contractual'),
        ('consultancy', 'Consultancy'),
        ('internship', 'Internship'),
    ]

    job_title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    reference_number = models.CharField(max_length=100, blank=True, help_text="e.g. PADEV/HR/VAC/2026/02")
    department = models.CharField(max_length=150, help_text="e.g. Engineering & Infrastructure")
    location = models.CharField(max_length=150, default='Monrovia HQ (with county travel)')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    description = models.TextField(help_text="Key responsibilities & role summary")
    requirements = models.TextField(help_text="Qualifications, experience & skills required")
    application_deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    contact_email = models.EmailField(default='hr@padev.org')
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description (max 160 chars)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Career Vacancy'
        verbose_name_plural = 'Career Vacancies'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.job_title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:career_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.job_title} ({self.department})"


class ContactSubmission(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'

    def __str__(self):
        return f"{self.full_name} - {self.subject} ({self.submitted_at.strftime('%Y-%m-%d')})"

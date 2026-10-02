"""
Export every content type in the database to CSV files.

    python manage.py export_content                    # writes ./content_export/*.csv
    python manage.py export_content --output-dir ./out  # choose the folder
    python manage.py export_content --only programme news

Column names follow the spreadsheet templates in PADEV_CONTENT_GUIDE.md section 12,
with the system keys ``id`` and (where the model has one) ``slug`` added first so the
export can be matched against the live records later.
"""

import csv
import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db.models.fields.files import FieldFile
from django.utils import timezone

from core import models


def _raw(field):
    """Plain value coercion for non-choice fields."""

    def reader(row):
        value = getattr(row, field)
        if value is None:
            return ''
        if isinstance(value, bool):
            return 'TRUE' if value else 'FALSE'
        if isinstance(value, FieldFile):
            return value.name or ''
        if hasattr(value, 'isoformat'):
            return value.isoformat()
        return str(value)

    return reader


def _choice(field):
    """Choice columns export the human label (see guide sections 10 and 15)."""
    return lambda row: getattr(row, 'get_%s_display' % field)()


def _local_date(value):
    if not value:
        return ''
    if timezone.is_aware(value):
        value = timezone.localtime(value)
    return value.strftime('%Y-%m-%d')


def _deadline(value):
    """Procurement closing time in the guide's format: 2026-10-31 17:00 (GMT+00:00)."""
    if not value:
        return ''
    if timezone.is_aware(value):
        value = timezone.localtime(value)
    offset = value.strftime('%z')
    offset = '%s:%s' % (offset[:3], offset[3:]) if offset else ''
    return '%s (GMT%s)' % (value.strftime('%Y-%m-%d %H:%M'), offset)


def _pk(row):
    return row.pk


def _slug(row):
    return row.slug or ''


# One entry per content type: key -> filename -> model -> (header, reader) columns.
SPECS = (
    {
        'key': 'site_settings',
        'filename': 'SiteSettings.csv',
        'model': models.SiteSetting,
        'columns': (
            ('id', _pk),
            ('site_name', _raw('site_name')),
            ('agency_acronym', _raw('agency_acronym')),
            ('contact_email', _raw('contact_email')),
            ('contact_phone', _raw('contact_phone')),
            ('address', _raw('address')),
            ('social_links', lambda r: json.dumps(r.social_links, ensure_ascii=False) if r.social_links else ''),
            ('logo', _raw('logo')),
            ('hero_background_image', _raw('hero_background_image')),
            ('hero_text', _raw('hero_text')),
            ('program_structure_heading', _raw('program_structure_heading')),
            ('program_structure_intro', _raw('program_structure_intro')),
            ('about_heading', _raw('about_heading')),
            ('about_intro', _raw('about_intro')),
            ('about_content', _raw('about_content')),
            ('about_mission', _raw('about_mission')),
            ('about_vision', _raw('about_vision')),
            ('about_values', _raw('about_values')),
            ('home_about_badge', _raw('home_about_badge')),
            ('home_about_heading', _raw('home_about_heading')),
            ('home_about_text', _raw('home_about_text')),
            ('home_about_badge_year', _raw('home_about_badge_year')),
            ('home_about_badge_label', _raw('home_about_badge_label')),
            ('home_about_highlight_1_title', _raw('home_about_highlight_1_title')),
            ('home_about_highlight_1_text', _raw('home_about_highlight_1_text')),
            ('home_about_highlight_2_title', _raw('home_about_highlight_2_title')),
            ('home_about_highlight_2_text', _raw('home_about_highlight_2_text')),
            ('home_about_image_1', _raw('home_about_image_1')),
            ('home_about_image_2', _raw('home_about_image_2')),
        ),
    },
    {
        'key': 'navigation',
        'filename': 'Navigation.csv',
        'model': models.NavigationMenu,
        'columns': (
            ('id', _pk),
            ('title', _raw('title')),
            ('url', _raw('url')),
            ('parent_title', lambda r: r.parent.title if r.parent_id else ''),
            ('order', _raw('order')),
            ('badge_text', _raw('badge_text')),
            ('is_active', _raw('is_active')),
        ),
    },
    {
        'key': 'hero',
        'filename': 'HeroSlide.csv',
        'model': models.HeroSlide,
        'columns': (
            ('id', _pk),
            ('slug', _slug),
            ('badge_text', _raw('badge_text')),
            ('title', _raw('title')),
            ('description', _raw('description')),
            ('detail_content', _raw('detail_content')),
            ('slide_image', _raw('slide_image')),
            ('order', _raw('order')),
            ('is_active', _raw('is_active')),
        ),
    },
    {
        'key': 'program_structure',
        'filename': 'ProgramStructure.csv',
        'model': models.ProgramStructure,
        'columns': (
            ('id', _pk),
            ('slug', _slug),
            ('title', _raw('title')),
            ('description', _raw('description')),
            ('detail_content', _raw('detail_content')),
            ('icon_class', _raw('icon_class')),
            ('theme', _choice('theme')),
            ('order', _raw('order')),
            ('is_active', _raw('is_active')),
        ),
    },
    {
        'key': 'programme',
        'filename': 'Program.csv',
        'model': models.Program,
        'columns': (
            ('id', _pk),
            ('slug', _slug),
            ('title', _raw('title')),
            ('icon_class', _raw('icon_class')),
            ('short_description', _raw('short_description')),
            ('description', _raw('description')),
            ('status', _choice('status')),
            ('county', _choice('county')),
            ('budget', _raw('budget')),
            ('target_beneficiaries', _raw('target_beneficiaries')),
            ('start_date', _raw('start_date')),
            ('end_date', _raw('end_date')),
            ('is_featured', _raw('is_featured')),
            ('meta_description', _raw('meta_description')),
            ('cover_image', _raw('cover_image')),
        ),
    },
    {
        'key': 'programme_photo',
        'filename': 'ProgramPhoto.csv',
        'model': models.ProgramImage,
        'columns': (
            ('id', _pk),
            ('program_slug', lambda r: r.program.slug if r.program_id else ''),
            ('image', _raw('image')),
            ('caption', _raw('caption')),
            ('sort_order', _raw('sort_order')),
        ),
    },
    {
        'key': 'project',
        'filename': 'Project.csv',
        'model': models.Project,
        'columns': (
            ('id', _pk),
            ('slug', _slug),
            ('title', _raw('title')),
            ('program_title', lambda r: r.program.title if r.program_id else ''),
            ('short_description', _raw('short_description')),
            ('description', _raw('description')),
            ('status', _choice('status')),
            ('county', _choice('county')),
            ('location_details', _raw('location_details')),
            ('progress_percentage', _raw('progress_percentage')),
            ('budget', _raw('budget')),
            ('contractor', _raw('contractor')),
            ('donor', _raw('donor')),
            ('implementing_agency', _raw('implementing_agency')),
            ('partners', _raw('partners')),
            ('report_link', _raw('report_link')),
            ('start_date', _raw('start_date')),
            ('completion_date', _raw('completion_date')),
            ('is_featured', _raw('is_featured')),
            ('meta_description', _raw('meta_description')),
            ('cover_image', _raw('cover_image')),
        ),
    },
    {
        'key': 'news',
        'filename': 'News.csv',
        'model': models.NewsUpdate,
        'columns': (
            ('id', _pk),
            ('slug', _slug),
            ('title', _raw('title')),
            ('author', _raw('author')),
            ('category', _choice('category')),
            ('excerpt', _raw('excerpt')),
            ('content_file', _raw('content')),
            ('approved_publication_date', _raw('published_date')),
            ('is_featured', _raw('is_featured')),
            ('meta_description', _raw('meta_description')),
            ('featured_image', _raw('featured_image')),
        ),
    },
    {
        'key': 'story',
        'filename': 'Story.csv',
        'model': models.SuccessStory,
        'columns': (
            ('id', _pk),
            ('slug', _slug),
            ('title', _raw('title')),
            ('beneficiary_name', _raw('beneficiary_name')),
            ('county', _choice('county')),
            ('quote', _raw('quote')),
            ('content_file', _raw('content')),
            ('consent_reference', lambda r: ''),
            ('is_featured', _raw('is_featured')),
            ('meta_description', _raw('meta_description')),
            ('featured_image', _raw('featured_image')),
        ),
    },
    {
        'key': 'team',
        'filename': 'Team.csv',
        'model': models.TeamMember,
        'columns': (
            ('id', _pk),
            ('full_name', _raw('full_name')),
            ('position', _raw('position')),
            ('role_category', _choice('role_category')),
            ('bio', _raw('bio')),
            ('photo', _raw('photo')),
            ('email', _raw('email')),
            ('order', _raw('order')),
            ('is_active', _raw('is_active')),
        ),
    },
    {
        'key': 'partner',
        'filename': 'Partner.csv',
        'model': models.Client,
        'columns': (
            ('id', _pk),
            ('name', _raw('name')),
            ('logo', _raw('logo')),
            ('website', _raw('website')),
            ('order', _raw('order')),
            ('is_active', _raw('is_active')),
            ('public_display_approved', lambda r: ''),
        ),
    },
    {
        'key': 'publication',
        'filename': 'Publication.csv',
        'model': models.Publication,
        'columns': (
            ('id', _pk),
            ('slug', _slug),
            ('title', _raw('title')),
            ('category', _choice('category')),
            ('description', _raw('description')),
            ('pdf_file', _raw('pdf_file')),
            ('cover_image', _raw('cover_image')),
            ('file_size', _raw('file_size')),
            ('publication_date', _raw('publication_date')),
            ('meta_description', _raw('meta_description')),
        ),
    },
    {
        'key': 'procurement',
        'filename': 'Procurement.csv',
        'model': models.ProcurementOpportunity,
        'columns': (
            ('id', _pk),
            ('slug', _slug),
            ('title', _raw('title')),
            ('reference_number', _raw('reference_number')),
            ('category', _choice('category')),
            ('description', _raw('description')),
            ('tender_document', _raw('tender_document')),
            ('opening_date', _raw('opening_date')),
            ('closing_deadline_with_timezone', lambda r: _deadline(r.closing_deadline)),
            ('status', _choice('status')),
            ('contact_email', _raw('contact_email')),
            ('submission_location', _raw('submission_location')),
            ('meta_description', _raw('meta_description')),
        ),
    },
    {
        'key': 'career',
        'filename': 'Career.csv',
        'model': models.Career,
        'columns': (
            ('id', _pk),
            ('slug', _slug),
            ('job_title', _raw('job_title')),
            ('reference_number', _raw('reference_number')),
            ('department', _raw('department')),
            ('location', _raw('location')),
            ('job_type', _choice('job_type')),
            ('description', _raw('description')),
            ('requirements', _raw('requirements')),
            ('application_deadline', _raw('application_deadline')),
            ('contact_email', _raw('contact_email')),
            ('is_active', _raw('is_active')),
            ('meta_description', _raw('meta_description')),
        ),
    },
)

README = """PADEV website content export
============================

Generated by: python manage.py export_content
Source: the live database (this folder is regenerated on every run and is not committed to git).

How the files are laid out
--------------------------
* One CSV per content type, named after the spreadsheet templates in
  PADEV_CONTENT_GUIDE.md section 12.
* The first column is always `id` (the record's database key) and, where the content
  type has one, the second is `slug` (the web address). Both are system values - do not
  rename or delete them. Every other column keeps the guide's field name unchanged.
* Dates are written as YYYY-MM-DD. Procurement closing times use the guide's format,
  for example 2026-10-31 17:00 (GMT+00:00), in local Monrovia time.
* TRUE / FALSE are used for yes/no columns.
* Choice columns (status, county, category, theme, role, job type) contain the human
  labels listed in sections 10 and 15 of the guide, for example "Nationwide / Multiple
  Counties" or "Press Release".
* Image and PDF columns contain the stored file path, for example
  "programs/forest-governance.jpg". The files themselves are not included; download them
  from the media library or Cloudinary separately.
* Long article text is kept inside the CSV (the guide's `content_file` columns), so a
  cell may contain several paragraphs - keep the line breaks.

Columns kept blank on purpose
-----------------------------
* Story.csv `consent_reference` and Partner.csv `public_display_approved`: the website
  has no field for these yet, so record them in the spreadsheet for the client's files.
* Publication.csv does not include `download_count`, which the guide marks as
  system-managed.
* Contact submissions are visitor enquiries and are never exported.

To export only some content types:
    python manage.py export_content --only programme news
Keys: {keys}
"""


class Command(BaseCommand):
    help = (
        'Export every content type in the database to CSV files, using the column '
        'names from PADEV_CONTENT_GUIDE.md section 12.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            default='content_export',
            help='Folder to write the CSV files into (default: content_export)',
        )
        parser.add_argument(
            '--only',
            nargs='*',
            metavar='KEY',
            help='Only export these content types, e.g. --only programme news',
        )

    def handle(self, *args, **options):
        specs = list(SPECS)

        only = options.get('only')
        if only:
            wanted = {key.lower() for key in only}
            known = {spec['key'] for spec in specs}
            unknown = sorted(wanted - known)
            if unknown:
                raise CommandError(
                    'Unknown content type(s): %s. Available: %s'
                    % (', '.join(unknown), ', '.join(sorted(known)))
                )
            specs = [spec for spec in specs if spec['key'] in wanted]

        out_dir = Path(options['output_dir'])
        out_dir.mkdir(parents=True, exist_ok=True)

        total_rows = 0
        for spec in specs:
            path = out_dir / spec['filename']
            headers = [header for header, _ in spec['columns']]
            rows = spec['model'].objects.all()
            count = 0
            with path.open('w', newline='', encoding='utf-8-sig') as handle:
                writer = csv.writer(handle)
                writer.writerow(headers)
                for row in rows:
                    writer.writerow([reader(row) for _, reader in spec['columns']])
                    count += 1
            total_rows += count
            self.stdout.write('%-24s %d row(s)' % (spec['filename'], count))

        readme = README.format(keys=', '.join(spec['key'] for spec in SPECS))
        (out_dir / 'README.txt').write_text(readme, encoding='utf-8')

        self.stdout.write(
            self.style.SUCCESS(
                'Exported %d file(s), %d row(s) -> %s'
                % (len(specs), total_rows, out_dir)
            )
        )

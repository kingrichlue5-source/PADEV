from django.db import migrations, models
from django.utils.text import slugify


def _fill_slugs_and_content(apps, schema_editor):
    """Give every existing slide/card a slug and a full detail article."""
    for model_name in ('heroslide', 'programstructure'):
        Model = apps.get_model('core', model_name)
        used = {s for s in Model.objects.values_list('slug', flat=True) if s}
        for obj in Model.objects.all():
            if not obj.slug:
                base = slugify(obj.title) or model_name
                slug, counter = base, 2
                while slug in used:
                    slug = f'{base}-{counter}'
                    counter += 1
                used.add(slug)
                obj.slug = slug
            if not obj.detail_content and obj.description:
                obj.detail_content = obj.description
            Model.objects.filter(pk=obj.pk).update(
                slug=obj.slug, detail_content=obj.detail_content,
            )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_seed_program_structure'),
    ]

    operations = [
        # Add the new columns (slug is nullable until every row is backfilled)
        migrations.AddField(
            model_name='heroslide',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='heroslide',
            name='detail_content',
            field=models.TextField(
                blank=True,
                default='',
                help_text="Full article shown on this slide's Read More page (new paragraphs start on a new line)",
            ),
        ),
        migrations.AddField(
            model_name='programstructure',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='programstructure',
            name='detail_content',
            field=models.TextField(
                blank=True,
                default='',
                help_text='Full article shown when the card title is clicked (new paragraphs start on a new line)',
            ),
        ),

        # Backfill slugs from titles and seed the detail pages with the existing copy
        migrations.RunPython(_fill_slugs_and_content, migrations.RunPython.noop),

        # Tighten the columns to match the model
        migrations.AlterField(
            model_name='heroslide',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='heroslide',
            name='detail_content',
            field=models.TextField(
                blank=True,
                help_text="Full article shown on this slide's Read More page (new paragraphs start on a new line)",
            ),
        ),
        migrations.AlterField(
            model_name='programstructure',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='programstructure',
            name='detail_content',
            field=models.TextField(
                blank=True,
                help_text='Full article shown when the card title is clicked (new paragraphs start on a new line)',
            ),
        ),

        # The hero CTA fields are replaced by the single "Read More" button
        migrations.RemoveField(model_name='heroslide', name='primary_cta_text'),
        migrations.RemoveField(model_name='heroslide', name='primary_cta_url'),
        migrations.RemoveField(model_name='heroslide', name='secondary_cta_text'),
        migrations.RemoveField(model_name='heroslide', name='secondary_cta_url'),
    ]

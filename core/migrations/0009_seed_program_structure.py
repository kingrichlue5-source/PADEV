from django.db import migrations

DEFAULT_CARDS = [
    {
        'title': 'Community Forest Governance',
        'description': 'Establishing and strengthening community forest governance entities with FDA and local leaders.',
        'icon_class': 'ri-tree-line',
        'theme': 'green',
        'order': 1,
    },
    {
        'title': 'Conservation Education',
        'description': 'Inspiring pupils through environmental clubs and community theater troupes.',
        'icon_class': 'ri-megaphone-line',
        'theme': 'gold',
        'order': 2,
    },
    {
        'title': 'Livelihood & Enterprise',
        'description': 'Conservation agriculture and beekeeping that raise incomes for forest-fringed communities.',
        'icon_class': 'ri-seedling-line',
        'theme': 'navy',
        'order': 3,
    },
    {
        'title': 'Gender & Social Inclusion',
        'description': 'Inclusion of women, boys, girls, and marginalized people in all project activities.',
        'icon_class': 'ri-women-line',
        'theme': 'rose',
        'order': 4,
    },
]


def seed_program_structure(apps, schema_editor):
    ProgramStructure = apps.get_model('core', 'ProgramStructure')
    if ProgramStructure.objects.exists():
        return
    for card in DEFAULT_CARDS:
        ProgramStructure.objects.create(**card, is_active=True)


def unseed_program_structure(apps, schema_editor):
    ProgramStructure = apps.get_model('core', 'ProgramStructure')
    ProgramStructure.objects.filter(
        title__in=[card['title'] for card in DEFAULT_CARDS],
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_programstructure'),
    ]

    operations = [
        migrations.RunPython(seed_program_structure, unseed_program_structure),
    ]

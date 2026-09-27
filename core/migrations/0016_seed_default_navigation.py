"""Give a brand-new database its standard navigation menu.

The menu is editable content, so this only ever runs when the menu table is
completely empty — once an editor has touched it, the menu is theirs.
"""
from django.db import migrations

DEFAULT_NAV = (
    ('Home', '/', 1),
    ('About Us', '/about/', 2),
    ('Our Team', '/team/', 3),
    ('Programmes', '/programmes/', 4),
    ('Projects', '/projects/', 5),
    ('Publications', '/publications/', 6),
    ('Contact Us', '/contact/', 7),
)


def seed_navigation(apps, schema_editor):
    NavigationMenu = apps.get_model('core', 'NavigationMenu')
    if NavigationMenu.objects.exists():
        return
    for title, url, order in DEFAULT_NAV:
        NavigationMenu.objects.create(title=title, url=url, order=order, is_active=True)


def remove_seeded_navigation(apps, schema_editor):
    NavigationMenu = apps.get_model('core', 'NavigationMenu')
    for title, url, order in DEFAULT_NAV:
        NavigationMenu.objects.filter(title=title, url=url, order=order).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_sitesetting_about_intro'),
    ]

    operations = [
        migrations.RunPython(seed_navigation, remove_seeded_navigation),
    ]

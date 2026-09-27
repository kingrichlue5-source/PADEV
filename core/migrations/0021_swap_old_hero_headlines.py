"""Put the client's rotating headlines on databases that still show the old one.

The previous migration only swapped records that matched the old default
character for character. A record written with different line endings or
trailing whitespace slipped through, so this pass matches on the headline text
itself instead — and still leaves anything an editor wrote alone.
"""
from django.db import migrations

OLD_DEFAULT = "Start Your Community's\n**Beautiful & Bright** Future."

NEW_DEFAULT = (
    "Empowering Communities. **Preserving Nature.** Securing Futures.\n\n"
    "The Future of **Sustainable Forest Management** Belongs to Communities…\n\n"
    "We partner with local communities to **sustainably manage their natural resources**, "
    "protecting biodiversity while building resilient local economies.\n\n"
    "Putting **A Human Face** to Community Forestry…\n\n"
    "We empower forest dependent communities to protect their forests, build **sustainable "
    "livelihoods**, and fight climate change from bottom, up.\n\n"
    "**Meet the Communities** and Support Our Mission\n\n"
    "Reaching **100+ Rural Communities**, leaving real impacts\n\n"
    "**Building infrastructure** with the people\n\n"
    "**Laying foundations** for growth\n\n"
    "**Building capacity** and leaving lasting legacy"
)

OLD_SNIPPET = 'Beautiful & Bright'


def swap_by_headline_text(apps, schema_editor):
    SiteSetting = apps.get_model('core', 'SiteSetting')
    for row in SiteSetting.objects.all():
        value = row.hero_text or ''
        normalized = value.replace('\r\n', '\n').replace('\r', '\n').strip()
        if OLD_SNIPPET in normalized and 'Empowering Communities' not in normalized:
            row.hero_text = NEW_DEFAULT
            row.save(update_fields=['hero_text'])


def restore_by_headline_text(apps, schema_editor):
    SiteSetting = apps.get_model('core', 'SiteSetting')
    for row in SiteSetting.objects.all():
        if (row.hero_text or '').strip() == NEW_DEFAULT:
            row.hero_text = OLD_DEFAULT
            row.save(update_fields=['hero_text'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_sitesetting_hero_text'),
    ]

    operations = [
        migrations.RunPython(swap_by_headline_text, restore_by_headline_text),
    ]

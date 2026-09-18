from django.test import TestCase
from django.core.management import call_command
from .models import SiteSetting, NavigationMenu, HeroSlide


class CmsContentTests(TestCase):
    def test_seed_data_creates_site_settings_and_menu_items(self):
        call_command('seed_data')

        self.assertTrue(SiteSetting.objects.exists())
        self.assertTrue(NavigationMenu.objects.filter(is_active=True).exists())
        self.assertTrue(HeroSlide.objects.filter(is_active=True).exists())

        site_settings = SiteSetting.objects.get()
        self.assertTrue(site_settings.site_name)
        self.assertTrue(site_settings.agency_acronym)

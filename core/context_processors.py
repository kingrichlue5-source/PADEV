from .models import SiteSetting, NavigationMenu


def site_settings(request):
    settings = SiteSetting.get_instance()
    nav_items = NavigationMenu.objects.filter(is_active=True, parent__isnull=True).order_by('order', 'title')
    return {
        'site_settings': settings,
        'nav_menus': nav_items,
    }

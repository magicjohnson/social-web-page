import cities_light

from social_web_page.settings import CITIES_LIGHT_INCLUDE_CITIES_FROM_COUNTRIES


def filter_city_import(sender, items, **kwargs):
    if items[8] not in CITIES_LIGHT_INCLUDE_CITIES_FROM_COUNTRIES:
        raise cities_light.InvalidItems()

cities_light.signals.city_items_pre_import.connect(filter_city_import)

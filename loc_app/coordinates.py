import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from geopy import distance

from loc_app.models import Location


def fetch_coordinates(address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": settings.YANDEX_API_KEY,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def check_or_create_loc(address):
    try:
        loc_address = Location.objects.get(address=address)

    except ObjectDoesNotExist:
        longitude, latitude = fetch_coordinates(address)
        loc_address, created = Location.objects.get_or_create(
            address=address,
            latitude=latitude,
            longitude=longitude,
            requested_at=timezone.now(),
        )

    return loc_address


def calculate_distance(order_address, restaurant_address):
    try:
        order_coordinates = check_or_create_loc(order_address)
        restaurant_coordinates = check_or_create_loc(restaurant_address)
    except (requests.HTTPError, requests.ConnectionError):
        return "Ошибка координат"

    order_distance = distance.distance(
        (order_coordinates.latitude, order_coordinates.longitude),
        (restaurant_coordinates.latitude, restaurant_coordinates.longitude),
    )
    return order_distance.km

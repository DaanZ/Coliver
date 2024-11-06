import json

import requests

from lodgify.api import lodgify_headers


def get_availability(property_id: int, room_id: int):
    url = f"https://api.lodgify.com/v1/availability/{property_id}/{room_id}?periodStart=2024-11-01T00%3A00%3A00Z&periodEnd=2024-11-30T00%3A00%3A00Z"
    response = requests.get(url, headers=lodgify_headers)
    availabilities = json.loads(response.text)
    available = []
    for period in availabilities:
        if period["available"] > 0:
            available.append(period)
    return available


if __name__ == "__main__":
    availables = get_availability(621023, 687929)
    print(availables)

import json
import requests

from lodgify.api import lodgify_headers


def get_rooms():
    response = requests.get("https://api.lodgify.com/v1/properties",
                            headers=lodgify_headers)
    return json.loads(response.text)


if __name__ == "__main__":
    r: list[dict[str, int]] = get_rooms()
    print(r)

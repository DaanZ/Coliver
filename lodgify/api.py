import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["LODGIFY_API_KEY"]

lodgify_headers = {
    "accept": "application/json",
    "X-ApiKey": API_KEY
}

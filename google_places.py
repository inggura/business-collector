import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

URL = "https://places.googleapis.com/v1/places:searchText"

HEADERS = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask":
        "places.id,"
        "places.displayName,"
        "places.formattedAddress,"
        "places.location,"
        "places.rating,"
        "places.userRatingCount,"
        "places.types"
}


def search_places(query):

    response = requests.post(
        URL,
        headers=HEADERS,
        json={"textQuery": query}
    )

    if response.status_code != 200:
        return []

    data = response.json()

    return data.get("places", [])
"""
API health checks for deployed VEDA backends using custom host endpoints
"""

import os

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()


def _get_link(obj: dict, rel: str) -> str:
    """get rel link from a stac object"""
    return next((link for link in obj.get("links") if link["rel"] == rel), None)


def test_stac_url_returns_200():
    custom_host = os.getenv("VEDA_CUSTOM_HOST")
    stac_root_path = os.getenv("VEDA_STAC_ROOT_PATH")
    health_endpoint = "_mgmt/ping"

    if not custom_host:
        pytest.skip("VEDA_CUSTOM_HOST not set. Skipping health test.")

    assert stac_root_path, "VEDA_STAC_ROOT_PATH must be set"

    url = f"https://{custom_host}/{stac_root_path.strip('/')}/{health_endpoint}"
    print(f"Checking custom host stac-api {url=}")
    response = requests.get(url)
    assert response.status_code == 200


def test_raster_url_returns_200():
    custom_host = os.getenv("VEDA_CUSTOM_HOST")
    raster_root_path = os.getenv("VEDA_RASTER_ROOT_PATH")
    health_endpoint = "healthz"

    if not custom_host:
        pytest.skip("VEDA_CUSTOM_HOST not set. Skipping health test.")

    assert raster_root_path, "VEDA_RASTER_ROOT_PATH must be set"

    url = f"https://{custom_host}/{raster_root_path.strip('/')}/{health_endpoint}"
    print(f"Checking custom host raster-api {url=}")
    response = requests.get(url)
    assert response.status_code == 200


def test_stac_item_next_link_returns_200():
    custom_host = os.getenv("VEDA_CUSTOM_HOST")
    stac_root_path = os.getenv("VEDA_STAC_ROOT_PATH")
    collections_endpoint = "collections"

    if not custom_host:
        pytest.skip("VEDA_CUSTOM_HOST not set. Skipping health test.")

    assert stac_root_path, "VEDA_STAC_ROOT_PATH must be set"

    url = f"https://{custom_host}/{stac_root_path.strip('/')}/{collections_endpoint}"
    print(f"Checking links for custom host stac-api {url=}")
    response = requests.get(url)
    assert response.status_code == 200

    # Walk check root path propagation through dynamic links when using custom host
    # and use a small page size so next links appear with fewer items
    collections = response.json().get("collections") or []

    if not collections:
        pytest.skip("No collections found in STAC catalog.")

    for collection in collections:
        items_link = _get_link(collection, "items")
        assert items_link
        items_url = items_link.get("href")
        assert items_url

        items_response = requests.get(items_url, params={"limit": 1})
        assert items_response.status_code == 200
        items_json = items_response.json()

        items_next_link = _get_link(items_json, "next")
        if not (items_next_link and items_next_link.get("href")):
            continue

        next_url = items_next_link["href"]
        next_response = requests.get(next_url)
        assert next_response.status_code == 200
        return

    print(f"Skipping. No collection 'next' items link found.")
    pytest.skip("No collection produced a paginated 'next' items link.")


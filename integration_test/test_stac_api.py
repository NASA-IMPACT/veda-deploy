import requests
from dotenv import load_dotenv
import os

load_dotenv()


def test_stac_url_returns_200():
    endpoint = os.getenv("STAC_URL")
    stac_path_prefix = os.getenv("VEDA_STAC_PATH_PREFIX")
    url = f"{endpoint.rstrip('/')}/{stac_path_prefix}/_mgmt/ping"
    response = requests.get(url)
    assert response.status_code == 200


def test_raster_url_returns_200():
    endpoint = os.getenv("RASTER_URL")
    url = f"{endpoint.rstrip('/')}/healthz"
    response = requests.get(url)
    assert response.status_code == 200

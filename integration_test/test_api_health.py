import requests
from dotenv import load_dotenv
import os

load_dotenv()


def test_stac_url_returns_200():
    base_url = os.getenv("VEDA_STAC_URL")
    stac_root_path = os.getenv("VEDA_STAC_ROOT_PATH")
    custom_host = os.getenv("VEDA_CUSTOM_HOST", None)
    health_endpoint = "_mgmt/ping"
    
    url = f"{base_url}{health_endpoint}"
    print(f"Checking APIGW stac-api {url=}")
    response = requests.get(url)
    assert response.status_code == 200

    if custom_host:
        url = f"https://{custom_host}/{stac_root_path.rstrip('/')}/{health_endpoint}"
        print(f"Checking custom host stac-api {url=}")
        response = requests.get(url)
        assert response.status_code == 200
    


def test_raster_url_returns_200():
    base_url = os.getenv("VEDA_RASTER_URL")
    raster_root_path = os.getenv("VEDA_RASTER_ROOT_PATH")
    custom_host = os.getenv("VEDA_CUSTOM_HOST", None)
    health_endpoint = "healthz"

    url = os.path.join(base_url, health_endpoint)
    print(f"Checking APIGW raster-api {url=}")
    response = requests.get(url)
    assert response.status_code == 200

    if custom_host:
        url = f"https://{custom_host}/{raster_root_path.rstrip('/')}/{health_endpoint}"
        print(f"Checking custom host raster-api {url=}")
        response = requests.get(url)
        assert response.status_code == 200

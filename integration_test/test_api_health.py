import requests
from dotenv import load_dotenv
import os

load_dotenv()

def _get_link(obj: dict, rel: str) -> str:
    """get rel link from a stac object"""
    return next((l for l in obj.get("links") if l["rel"]==rel), None)

def test_stac_url_returns_200():
    base_url = os.getenv("VEDA_STAC_URL")
    stac_root_path = os.getenv("VEDA_STAC_ROOT_PATH")
    custom_host = os.getenv("VEDA_CUSTOM_HOST", None)
    disable_default_apigw = os.getenv("VEDA_DISABLE_DEFAULT_APIGW_ENDPOINT", False)
    health_endpoint = "_mgmt/ping"
    
    if not disable_default_apigw:
        url = f"{base_url}{health_endpoint}" # APIGW base url includes trailing /
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
    disable_default_apigw = os.getenv("VEDA_DISABLE_DEFAULT_APIGW_ENDPOINT", False)
    health_endpoint = "healthz"

    if not disable_default_apigw:
        url = os.path.join(base_url, health_endpoint)
        print(f"Checking APIGW raster-api {url=}")
        response = requests.get(url)
        assert response.status_code == 200

    if custom_host:
        url = f"https://{custom_host}/{raster_root_path.rstrip('/')}/{health_endpoint}"
        print(f"Checking custom host raster-api {url=}")
        response = requests.get(url)
        assert response.status_code == 200

def test_stac_item_next_link_returns_200():
    base_url = os.getenv("VEDA_STAC_URL")
    stac_root_path = os.getenv("VEDA_STAC_ROOT_PATH")
    custom_host = os.getenv("VEDA_CUSTOM_HOST", None)
    disable_default_apigw = os.getenv("VEDA_DISABLE_DEFAULT_APIGW_ENDPOINT", False)
    collections_endpoint = "collections"
    
    if not disable_default_apigw:
        url = f"{base_url}/{collections_endpoint}"
        print(f"Checking APIGW stac-api {url=}")
        response = requests.get(url)
        assert response.status_code == 200

    if custom_host:
        url = f"https://{custom_host}/{stac_root_path.rstrip('/')}/{collections_endpoint}"
        print(f"Checking links for custom host stac-api {url=}")
        response = requests.get(url)
        assert response.status_code == 200
    
        # Walk check root path propagation through dynamic links when using custom host
        collections = response.json().get("collections")
        next_links_untested = True

        while next_links_untested:
            for collection in collections:
    
                # All collections should have a dynamicaly generateed items link, even if no items exist
                items_link = _get_link(collection, "items")
                assert items_link
                items_url = items_link.get("href")
                assert items_url
                items_response = requests.get(items_url)
                assert items_response.status_code == 200
                items_json = items_response.json()
                features = items_json.get("features")
            
                # The default page size is 10
                if len(features) >= 10:
                    items_next_link = _get_link(items_json, "next")
                    assert items_next_link
                    next_url = items_next_link.get("href")
                    assert next_url
                    next_response = requests.get(next_url)
                    assert next_response.status_code == 200
                    next_links_untested = False
                    break

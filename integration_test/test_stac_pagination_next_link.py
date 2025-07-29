import requests
from dotenv import load_dotenv
import os
import pytest

load_dotenv()

def _get_link(obj: dict, rel: str) -> str:
    """
    Helper function to find a specific link by its 'rel' type in a STAC object's "links" array.
    """
    if not obj or not obj.get("links"):
        return None
    return next((link for link in obj.get("links") if link.get("rel") == rel), None)

def test_collection_pagination_next_link_is_valid():
    """
    Validates that for collections with enough items to require pagination,
    the 'next' link provided in the item list is a valid URL that returns a 200 OK status.

    This test fetches all collections and then individually checks their item lists for pagination links.
    It focuses on the custom host configuration as it's the primary way
    dynamically generated links are used by end-users.
    """
    custom_host = os.getenv("VEDA_CUSTOM_HOST")
    stac_root_path = os.getenv("VEDA_STAC_ROOT_PATH", "")

    if not custom_host:
        pytest.skip("VEDA_CUSTOM_HOST environment variable not set. Skipping pagination test.")

    #  Construct the URL to the main collections endpoint
    collections_url = f"https://{custom_host}/{stac_root_path.strip('/')}/collections"
    print(f"Starting pagination test. Fetching collections from: {collections_url}")

    # Fetch all collections
    try:
        collections_response = requests.get(collections_url)
        collections_response.raise_for_status()  # Fail fast if collections endpoint is down
        collections = collections_response.json().get("collections", [])
    except (requests.exceptions.RequestException, ValueError) as e:
        pytest.fail(f"Could not fetch or parse collections from {collections_url}. Error: {e}")

    found_and_tested_a_next_link = False

    # Iterate through each collection to find one with pagination
    for collection_summary in collections:
        collection_id = collection_summary.get("id")
        if not collection_id:
            print("Skipping a collection that is missing an 'id'.")
            continue

        # Get the link to the collection's items. The 'items' link is within the collection's own links.
        items_link = _get_link(collection_summary, "items")
        if not (items_link and items_link.get("href")):
            print(f"Skipping collection '{collection_id}': No 'items' link found.")
            continue

        items_url = items_link["href"]
        print(f"Checking items for collection '{collection_id}' at: {items_url}")

        # Fetch the first page of items for the collection
        try:
            items_response = requests.get(items_url)
            if items_response.status_code != 200:
                print(f"Warning: Could not fetch items for '{collection_id}'. Status: {items_response.status_code}")
                continue
            items_json = items_response.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Warning: Could not fetch or parse items for '{collection_id}'. Error: {e}")
            continue

        # Check if a 'next' link exists on the first page of items
        next_link = _get_link(items_json, "next")
        if next_link and next_link.get("href"):
            next_url = next_link["href"]
            print(f"  - Found 'next' link: {next_url}")

            # Make a GET request to the 'next' URL
            try:
                next_page_response = requests.get(next_url)
                
                # Assert that the link is valid and returns a 200 OK status
                assert next_page_response.status_code == 200, f"'next' link for {collection_id} failed with status {next_page_response.status_code}"
                print(f"  - Success! 'next' link returned status {next_page_response.status_code}.")
                
                found_and_tested_a_next_link = True
                
                # Once we've successfully tested one 'next' link, we can exit to keep the test fast.
                break
            except requests.exceptions.RequestException as e:
                pytest.fail(f"Request for 'next' link URL {next_url} failed. Error: {e}")
        else:
            print(f"  - No 'next' link found for '{collection_id}' (collection may have less than one page of items).")

    # Final assertion to ensure the test actually performed a validation.
    # If this fails, it means no collections with pagination were found across the entire API.
    assert found_and_tested_a_next_link, "Test finished without finding any collection with a 'next' link to validate."

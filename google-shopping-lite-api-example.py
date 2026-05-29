"""
Google Shopping Lite API: A Quick Start Example
See more at: https://apify.com/johnvc/google-shopping-lite-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/google-shopping-lite-api/input-schema?fpr=9n7kx3

This script shows how to call the Google Shopping Lite API on Apify from Python
and read its structured JSON output. The API returns one row per product, each
with the title, price, retailer, rating, delivery note, and a link. It exercises
every input parameter so you can see what is configurable, while keeping the run
small so your first call stays cheap.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
"""

import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

# Initialize the Apify client with your API token (read from .env)
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Build the Actor input.
# Values are kept small (one search term, maxResultsPerSearch=10) to keep this
# first run inexpensive. Raise them once you have your own API key and budget.
run_input = {
    "searchTerms": ["wireless headphones"],  # add more terms to search several at once
    "country": "us",                          # ISO 3166-1 two-letter country code
    "language": "en",                         # ISO 639-1 two-letter language code
    "maxResultsPerSearch": 10,                # products per term; the API paginates up to this cap
}

# Run the Actor and wait for it to finish.
run = client.actor("johnvc/google-shopping-lite-api").call(run_input=run_input)
if run is None:
    raise SystemExit("The Actor run did not return a result.")

# Read structured results from the run's default dataset.
# (apify-client 3.x returns a Run object; use .default_dataset_id, not run["..."])
items = list(client.dataset(run.default_dataset_id).iterate_items())
print(f"Returned {len(items)} product(s).\n")

# Show a few key fields from each product. Each dataset item is one product.
for item in items:
    if item.get("result_type") != "product":
        continue  # skip any error rows
    print(f"- {item.get('title')}")
    print(f"    price:  {item.get('price')}    retailer: {item.get('source')}")
    print(f"    rating: {item.get('rating')} ({item.get('ratingCount')} ratings)")
    print(f"    search: {item.get('searchQuery')}")
    print(f"    link:   {item.get('link')}\n")

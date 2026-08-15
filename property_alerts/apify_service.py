from __future__ import annotations

import os
import re
from typing import Any


DEFAULT_ACTOR_ID = "scrapesage/propertyguru-scraper"


def parse_search_queries(query_text: str) -> list[str]:
    """Normalize user input into a clean list of search queries."""
    if query_text is None:
        return []

    raw_values = re.split(r"[\n,]+", query_text)
    normalized: list[str] = []
    seen: set[str] = set()

    for value in raw_values:
        cleaned = " ".join(value.strip().split())
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(cleaned)

    return normalized


def build_actor_payload(
    search_queries: list[str],
    listing_type: str = "sale",
    min_price: int | None = None,
    include_listing_details: bool = True,
    include_agent_leads: bool = True,
    max_items: int = 200,
) -> dict[str, Any]:
    """Build the exact payload required by the Apify PropertyGuru scraper actor."""
    payload: dict[str, Any] = {
        "searchQueries": list(search_queries),
        "listingType": listing_type,
        "includeListingDetails": include_listing_details,
        "includeAgentLeads": include_agent_leads,
        "maxItems": max_items,
    }
    if min_price is not None:
        payload["minPrice"] = int(min_price)
    return payload


def get_apify_token(token: str | None = None) -> str:
    resolved = token or os.getenv("APIFY_TOKEN") or os.getenv("APIFY_API_TOKEN")
    if not resolved:
        raise ValueError(
            "APIFY_TOKEN is missing. Add it to your environment or .env file before running the search."
        )
    return resolved


def run_property_search(
    search_queries: list[str],
    listing_type: str = "sale",
    min_price: int | None = None,
    include_listing_details: bool = True,
    include_agent_leads: bool = True,
    max_items: int = 200,
    actor_id: str = DEFAULT_ACTOR_ID,
    token: str | None = None,
) -> list[dict[str, Any]]:
    """Execute the scraper actor and return normalized listing objects."""
    from apify_client import ApifyClient

    client = ApifyClient(token=get_apify_token(token))
    payload = build_actor_payload(
        search_queries=search_queries,
        listing_type=listing_type,
        min_price=min_price,
        include_listing_details=include_listing_details,
        include_agent_leads=include_agent_leads,
        max_items=max_items,
    )

    run = client.actor(actor_id).call(run_input=payload)
    dataset_id = (run or {}).get("defaultDatasetId")
    if not dataset_id:
        raise RuntimeError("The Apify run did not return a default dataset ID.")

    response = client.dataset(dataset_id).list_items()
    if isinstance(response, dict):
        return response.get("items", [])
    return list(response) if response else []

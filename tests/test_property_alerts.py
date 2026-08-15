import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from property_alerts.apify_service import build_actor_payload, parse_search_queries


def test_parse_search_queries_handles_csv_and_newlines():
    query_text = "Bukit Timah, Orchard\nClementi"

    result = parse_search_queries(query_text)

    assert result == ["Bukit Timah", "Orchard", "Clementi"]


def test_build_actor_payload_uses_expected_apify_schema():
    payload = build_actor_payload(
        search_queries=["Bukit Timah", "Orchard"],
        listing_type="sale",
        min_price=2000000,
        include_listing_details=True,
        include_agent_leads=True,
        max_items=200,
    )

    assert payload == {
        "searchQueries": ["Bukit Timah", "Orchard"],
        "listingType": "sale",
        "minPrice": 2000000,
        "includeListingDetails": True,
        "includeAgentLeads": True,
        "maxItems": 200,
    }

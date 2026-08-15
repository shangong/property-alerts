from __future__ import annotations

import csv
import io
import os

import streamlit as st
from dotenv import load_dotenv

from property_alerts.apify_service import parse_search_queries, run_property_search


load_dotenv()


def _rows_to_csv(rows: list[dict]) -> str:
    if not rows:
        return ""

    fieldnames = list(rows[0].keys())
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def main() -> None:
    st.set_page_config(page_title="Property Alerts", page_icon="🏠", layout="wide")
    st.title("Property Alerts for Singapore")
    st.caption("Apify-powered PropertyGuru monitoring with a lightweight Streamlit UI.")

    with st.sidebar:
        st.header("Settings")
        apify_token = st.text_input(
            "Apify token",
            type="password",
            value=os.getenv("APIFY_TOKEN", ""),
            help="Set this in your environment or a .env file as APIFY_TOKEN.",
        )
        listing_type = st.selectbox("Listing type", options=["sale", "rent"], index=0)
        min_price = st.number_input("Minimum price", min_value=0, step=100000, value=2000000)
        max_items = st.number_input("Max listings", min_value=1, max_value=500, value=200, step=10)
        include_listing_details = st.checkbox("Include listing details", value=True)
        include_agent_leads = st.checkbox("Include agent leads", value=True)

    st.subheader("Search Queries")
    query_text = st.text_area(
        "Enter one query per line or comma-separated values",
        value="Bukit Timah\nOrchard\nClementi",
        height=160,
    )

    if st.button("Run property search", type="primary"):
        queries = parse_search_queries(query_text)
        if not queries:
            st.warning("Add at least one search query before running the scraper.")
            return

        try:
            results = run_property_search(
                search_queries=queries,
                listing_type=listing_type,
                min_price=int(min_price),
                include_listing_details=include_listing_details,
                include_agent_leads=include_agent_leads,
                max_items=int(max_items),
                token=apify_token or None,
            )
            if not results:
                st.info("No listings were returned for the selected filters.")
                return

            st.success(f"Fetched {len(results)} listing records.")
            st.dataframe(results, use_container_width=True)

            csv_data = _rows_to_csv(results).encode("utf-8")
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="property-alerts-results.csv",
                mime="text/csv",
            )
        except Exception as exc:  # pragma: no cover - UI surface only
            st.error(f"Search failed: {exc}")


if __name__ == "__main__":
    main()

# Property Alerts

A Python + Streamlit app for monitoring Singapore property listings through the Apify PropertyGuru scraper.

## Overview

This project replaces the earlier Google Alerts concept with a more reliable PropertyGuru data pipeline powered by Apify.

The app accepts one or more search queries, calls the Apify actor for PropertyGuru listings, and surfaces the results in a simple dashboard.

## Features

- Search by one or more areas or keywords
- Filter by sale or rent
- Set a minimum price threshold
- Include listing details and agent leads
- Download results as CSV
- Run as a local Streamlit dashboard

## Setup

1. Create a virtual environment (optional but recommended):
   python -m venv .venv
   source .venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Add your Apify token:
   cp .env.example .env
   Update APIFY_TOKEN in .env

4. Run the app:
   streamlit run app.py

## Example query input

Bukit Timah, Orchard
Clementi

## Apify request shape

The app sends the same payload structure described in the spec:

{
  "searchQueries": ["Bukit Timah", "Orchard"],
  "listingType": "sale",
  "minPrice": 2000000,
  "includeListingDetails": true,
  "includeAgentLeads": true,
  "maxItems": 200
}

## Notes

This project is intended for experimentation and internal monitoring use. Please ensure you comply with the source platform's terms and your Apify account usage conditions before running production data collection.

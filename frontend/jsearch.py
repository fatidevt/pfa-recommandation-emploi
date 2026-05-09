import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

API_KEY = os.getenv("JSEARCH_API_KEY")

def fetch_jobs(query="developer", location="Morocco", num_pages=1):
    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    all_jobs = []

    for page in range(1, num_pages + 1):
        params = {
            "query": f"{query} in {location}",
            "page": str(page),
            "num_pages": "1",
            "country": "ma"
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            jobs = data.get("data", [])
            all_jobs.extend(jobs)
            print(f"✅ Page {page}: {len(jobs)} jobs fetched")
        else:
            print(f"❌ Error on page {page}: {response.status_code} - {response.text}")
            break

    return all_jobs
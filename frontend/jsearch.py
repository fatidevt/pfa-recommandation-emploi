import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("JSEARCH_API_KEY")

def fetch_jobs(query="developer", location="Morocco", num_pages=1):
    """
    Fetch job offers from JSearch API.
    
    Args:
        query (str): Job title or keywords
        location (str): Job location
        num_pages (int): Number of result pages to fetch
    
    Returns:
        list: List of job offers in JSON format
    """
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
            "country": "ma"  # Morocco country code
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


def save_jobs_to_json(jobs, filename="jobs.json"):
    """Save jobs list to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)
    print(f"💾 {len(jobs)} jobs saved to {filename}")


if __name__ == "__main__":
    # Example: fetch developer jobs in Morocco
    jobs = fetch_jobs(query="software developer", location="Morocco", num_pages=2)

    if jobs:
        # Print first job as sample
        print("\n📋 Sample job:")
        print(json.dumps(jobs[0], indent=2))

        # Save all jobs to file
        save_jobs_to_json(jobs)
    else:
        print("No jobs found.")
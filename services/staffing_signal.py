import datetime
import http.client
import json
import typing
import requests
from typing import Dict, Any, List
from domain.models import Signal, Company
import os

def get_headcount(company: Company) -> int:
    url = f"https://api.harmonic.ai/companies?website_domain={company.domain}"
    headers = {
        "accept": "application/json",
        "apikey": "---",
    }
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        headcount = data.get("headcount", 0)
    except requests.RequestException as e:
        print(f"Error fetching headcount for {company.domain}: {str(e)}")
        headcount = 0
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response for {company.domain}: {str(e)}")
        headcount = 0
    return headcount

class PDLClient:
    def __init__(self):
        self.headers = {
            "X-Api-Key": "----",
            "X-Api-Token": "----",
        }

    def get_job_openings(self, domain: str) -> int:
        conn = http.client.HTTPSConnection("predictleads.com")
        try:
            conn.request(
                "GET", f"/api/v3/companies/{domain}/job_openings", headers=self.headers
            )
            res = conn.getresponse()
            data = json.loads(res.read().decode("utf-8"))
            job_listings = data.get("data", [])
            return len(job_listings)
        finally:
            conn.close()

    def get_data(self, domain: str) -> Dict[str, Any]:
        conn = http.client.HTTPSConnection("predictleads.com")
        try:
            conn.request("GET", f"/api/v3/companies/{domain}", headers=self.headers)
            res = conn.getresponse()
            data = json.loads(res.read().decode("utf-8"))
            return data
        finally:
            conn.close()


pdl_client = PDLClient()

def load_prev_job_counts(file_path: str) -> Dict[str, int]:
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

def save_prev_job_counts(file_path: str, prev_job_counts: Dict[str, int]):
    with open(file_path, "w") as f:
        json.dump(prev_job_counts, f, indent=4)

def generate_staffing_signals(
    pdl_client: PDLClient, companies: List[Company], prev_job_counts: dict
) -> typing.Iterable[Signal]:
    """
    Generate staffing signals based on job openings for companies,
    comparing to previous counts
    """

    for company in companies:
        if (get_headcount(company) != 0):
            headcount = "Headcounter:" + str(get_headcount(company))
        else:
            headcount = ""
        data = pdl_client.get_data(company.domain)
        with open(f"./.data/{company.domain}.json", "w") as f:
            json.dump(data, f, indent=4)
        try:
            current_openings = pdl_client.get_job_openings(company.domain)
            prev_openings = prev_job_counts.get(company.domain, 0)

            if current_openings > prev_openings:
                change = "increased"
                magnitude = (
                    "significantly " if current_openings - prev_openings > 10 else ""
                )
            elif current_openings < prev_openings:
                change = "decreased"
                magnitude = (
                    "significantly " if prev_openings - current_openings > 10 else ""
                )
            else:
                change = "remained the same"
                magnitude = ""

            if current_openings != prev_openings:
                signal = Signal(
                    id=f"staffing_{company.domain}_{datetime.datetime.now().isoformat()}",  # Generate unique ID
                    start_time=datetime.datetime.now(),
                    end_time=datetime.datetime.now(),
                    title=f"Job Openings Changed for {company.name}",
                    description=f"{headcount}\nJob openings {magnitude}{change} from {prev_openings} to {current_openings}",
                    company=company.model_dump(),
                )
                yield signal

            # Update previous count for next comparison
            prev_job_counts[company.domain] = current_openings

        except Exception as e:
            print(f"Error getting job openings for {company.domain}: {str(e)}")


if __name__ == "__main__":
    companies = [
        Company(
            name="Example Company",
            domain="google.com",
            linkedin_url=None,
            description="A great company",
            industry="Tech",
            location="San Francisco, CA",
            primary_contact=None,
        )
    ]
    prev_job_counts_file = "./.data/prev_job_counts.json"
    prev_job_counts = load_prev_job_counts(prev_job_counts_file)
    for signal in generate_staffing_signals(pdl_client, companies, prev_job_counts):
        print(signal)
    save_prev_job_counts(prev_job_counts_file, prev_job_counts)
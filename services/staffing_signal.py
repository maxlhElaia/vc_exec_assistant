import datetime
import http.client
import json
import typing
from typing import Dict, Any, List
from domain.models import Signal, Company

class PDLClient:
    def __init__(self):
        self.headers = {
            'X-Api-Key': "----",
            'X-Api-Token': "----",
        }
        
    def get_job_openings(self, domain: str) -> int:
        conn = http.client.HTTPSConnection("predictleads.com")
        try:
            conn.request("GET", f"/api/v3/companies/{domain}/job_openings", 
                        headers=self.headers)
            res = conn.getresponse()
            data = json.loads(res.read().decode("utf-8"))
            job_listings = data.get('data', [])
            return len(job_listings)
        finally:
            conn.close()
    
    def get_data(self, domain: str) -> Dict[str, Any]:
        conn = http.client.HTTPSConnection("predictleads.com")
        try:
            conn.request("GET", f"/api/v3/companies/{domain}", 
                        headers=self.headers)
            res = conn.getresponse()
            data = json.loads(res.read().decode("utf-8"))
            return data
        finally:
            conn.close()

pdl_client = PDLClient()

def generate_staffing_signals(pdl_client: PDLClient, 
                            companies: List[Company], 
                            prev_job_counts: dict) -> typing.Iterable[Signal]:
    """
    Generate staffing signals based on job openings for companies, 
    comparing to previous counts
    """

    for company in companies:
        data = pdl_client.get_data(company.domain)
        with open(f"./.data/{company.domain}.json", "w") as f:
            json.dump(data, f, indent=4)
        try:
            current_openings = pdl_client.get_job_openings(company.domain)
            prev_openings = prev_job_counts.get(company.domain, 0)

            if current_openings > prev_openings:
                change = "increased"
                magnitude = "significantly " if current_openings - prev_openings > 10 else ""
            elif current_openings < prev_openings:
                change = "decreased"
                magnitude = "significantly " if prev_openings - current_openings > 10 else ""
            else:
                change = "remained the same"
                magnitude = ""
            
            if current_openings != prev_openings:
                signal = Signal(
                    id=f"staffing_{company.domain}_{datetime.datetime.now().isoformat()}", # Generate unique ID
                    start_time=datetime.datetime.now(),
                    end_time=datetime.datetime.now(), 
                    title=f"Job Openings Changed for {company.name}",
                    description=f"Job openings {magnitude}{change} from {prev_openings} to {current_openings}",
                    company=company.model_dump()
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
            primary_contact=None
        )
    ]
    prev_job_counts = {}
    for signal in generate_staffing_signals(pdl_client, companies, prev_job_counts):
        print(signal)

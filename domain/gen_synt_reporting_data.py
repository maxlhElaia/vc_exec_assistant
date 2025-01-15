import json  
import random  
from datetime import datetime, timedelta  
  
# Define company profiles  
companies = [  
    {'name': 'FastGrower1', 'profile': 'very_fast_growth'},  
    {'name': 'FastGrower2', 'profile': 'very_fast_growth'},  
    {'name': 'UpDown1', 'profile': 'up_down'},  
    {'name': 'UpDown2', 'profile': 'up_down'},  
    {'name': 'UpDown3', 'profile': 'up_down'},  
    {'name': 'SlowGrower1', 'profile': 'slow_growth'},  
    {'name': 'SlowGrower2', 'profile': 'slow_growth'},  
    {'name': 'SlowGrower3', 'profile': 'slow_growth'},  
    {'name': 'Decliner1', 'profile': 'declining'},  
    {'name': 'Decliner2', 'profile': 'declining'}  
]  
  
# Function to generate synthetic data based on profile  
def generate_company_data(company):  
    data = []  
    start_date = datetime(2019, 1, 1)  
      
    # Initialize starting values  
    revenue = random.uniform(5000, 10000)  
    cash = random.uniform(50000, 200000)  # Lower initial cash for decliners  
    ebitda = revenue * random.uniform(-0.2, 0.2)  
    staff = random.randint(5, 20)  
    clients = random.randint(10, 50)  
    arr = revenue * 12  
  
    for month in range(60):  
        date = start_date + timedelta(days=30*month)  
        runway = cash / (-ebitda) if ebitda < 0 else float('inf')  
  
        # Modify metrics based on company profile  
        if company['profile'] == 'very_fast_growth':  
            growth_multiplier = 1 + random.uniform(0.05, 0.15)  
        elif company['profile'] == 'slow_growth':  
            growth_multiplier = 1 + random.uniform(0.01, 0.05)  
        elif company['profile'] == 'up_down':  
            growth_multiplier = 1 + random.uniform(-0.1, 0.1)  
        elif company['profile'] == 'declining':  
            growth_multiplier = 1 - random.uniform(0.05, 0.15)  
  
        # Update financials  
        revenue *= growth_multiplier  
        ebitda = revenue * random.uniform(-0.2, 0.2)  
        cash += ebitda  # Cash changes by EBITDA  
  
        # Check if the company has died  
        if cash <= 0:  
            print(f"{company['name']} has run out of cash and is now defunct.")  
            break  
  
        # Update other metrics  
        staff = max(1, int(staff * growth_multiplier))  
        clients = max(0, int(clients * growth_multiplier))  
        arr = revenue * 12  
        runway = cash / (-ebitda) if ebitda < 0 else float('inf')  
  
        data.append({  
            'date': date.strftime('%Y-%m'),  
            'revenues': round(revenue, 2),  
            'cash_eop': round(cash, 2),  
            'ebitda': round(ebitda, 2),  
            'runway_months': round(runway, 2) if runway != float('inf') else 'infinite',  
            'staff': staff,  
            'clients': clients,  
            'arr': round(arr, 2)  
        })  
  
    return data  
  
# Generate data for all companies  
all_data = {}  
for company in companies:  
    all_data[company['name']] = generate_company_data(company)  
  
# Save data to JSON file  
with open('./domain/synthetic_startup_data.json', 'w') as f:  
    json.dump(all_data, f, indent=4)  
  
print('Synthetic data generated and saved to synthetic_startup_data.json')  
import json  
import random  
from datetime import datetime, timedelta  
  
# Define company profiles with consistent growth rates  
companies = [  
    {'name': 'FastGrower1', 'profile': 'very_fast_growth', 'growth_rate': 0.10},  
    {'name': 'FastGrower2', 'profile': 'very_fast_growth', 'growth_rate': 0.12},  
    {'name': 'UpDown1', 'profile': 'up_down', 'growth_rate': 0.0},  
    {'name': 'UpDown2', 'profile': 'up_down', 'growth_rate': 0.0},  
    {'name': 'UpDown3', 'profile': 'up_down', 'growth_rate': 0.0},  
    {'name': 'SlowGrower1', 'profile': 'slow_growth', 'growth_rate': 0.03},  
    {'name': 'SlowGrower2', 'profile': 'slow_growth', 'growth_rate': 0.02},  
    {'name': 'SlowGrower3', 'profile': 'slow_growth', 'growth_rate': 0.01},  
    {'name': 'Decliner1', 'profile': 'declining', 'growth_rate': -0.05},  
    {'name': 'Decliner2', 'profile': 'declining', 'growth_rate': -0.07}  
]  
  
# Function to generate synthetic data based on profile  
def generate_company_data(company):  
    data = []  
    start_date = datetime(2019, 1, 1)  
      
    # Initialize starting values  
    revenue = random.uniform(5000, 10000)  
    cash = random.uniform(50000, 200000)  
    staff = random.randint(5, 20)  
    clients = random.randint(10, 50)  
    arr = revenue * 12  
      
    # Assign an initial EBITDA margin that changes slowly over time  
    if company['profile'] == 'very_fast_growth' or company['profile'] == 'slow_growth':  
        ebitda_margin = random.uniform(-0.1, 0.1)  # Start close to breakeven  
    elif company['profile'] == 'up_down':  
        ebitda_margin = random.uniform(-0.2, 0.2)  
    elif company['profile'] == 'declining':  
        ebitda_margin = random.uniform(-0.2, -0.1)  # Likely negative  
      
    for month in range(60):  
        date = start_date + timedelta(days=30*month)  
          
        # Adjust EBITDA margin slowly over time  
        ebitda_margin_change = random.uniform(-0.01, 0.01)  # Small change each month  
        ebitda_margin += ebitda_margin_change  
        ebitda_margin = max(min(ebitda_margin, 0.2), -0.2)  # Keep it within [-20%, 20%]  
          
        # Adjust revenue based on growth rate with minor randomness  
        growth_rate = company['growth_rate']  
        randomness = random.uniform(-0.005, 0.005)  # Minor randomness  
        revenue *= (1 + growth_rate + randomness)  
          
        # Update EBITDA based on new margin  
        ebitda = revenue * ebitda_margin  
          
        # Update cash  
        cash += ebitda  # Cash changes by EBITDA  
          
        # Check if the company has run out of cash  
        if cash <= 0:  
            print(f"{company['name']} has run out of cash and is now defunct.")  
            break  
          
        # Adjust staff and clients proportional to revenue growth  
        staff = max(1, int(staff * (1 + growth_rate + randomness)))  
        clients = max(0, int(clients * (1 + growth_rate + randomness)))  
          
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
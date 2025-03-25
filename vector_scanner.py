import json
import requests
import argparse
from time import sleep
import webbrowser

# Function to load the configuration file
def load_config(file_path):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config

# Load the configuration
config = load_config('config.json')

# Use the configuration parameters
API_KEY = config['api_key']
API_URL = config['api_url']

BANNER = """
██╗   ██╗███████╗ ██████╗████████╗ ██████╗ ██████╗ 
██║   ██║██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
██║   ██║█████╗  ██║        ██║   ██║   ██║██████╔╝
╚██╗ ██╔╝██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
 ╚████╔╝ ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
  ╚═══╝  ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
"""

def legal_confirmation():
    print(BANNER)
    print("\n[!] LEGAL COMPLIANCE REQUIRED")
    confirm = input("Do you have written consent? (yes/no): ").lower()
    if confirm not in ('yes', 'y'):
        print("\n[!] Scan aborted - Consent required")
        exit()

def ethical_scan(number):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'number': number
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        
        print("\n[+] Validated Information:")
        print(f"Number: {data.get('number')}")
        print(f"Valid: {data.get('valid')}")
        print(f"Country: {data.get('country_name')}")
        print(f"Carrier: {data.get('carrier')}")
    else:
        print(f"\n[!] Failed to validate number. Status Code: {response.status_code}")

def social_media_check(number):
    print("\n[+] Public Profile Check:")
    platforms = {
        "Truecaller": f"https://www.truecaller.com/search/in/{number}",
        "Facebook": f"https://www.facebook.com/{number}",
        "WhatsApp": f"https://wa.me/{number}"
    }
    
    for name, url in platforms.items():
        try:
            if requests.get(url).status_code == 200:
                print(f"{name}: Profile exists (manual verification required)")
        except requests.RequestException:
            pass

if __name__ == "__main__":
    legal_confirmation()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("number", help="Phone number with country code")
    args = parser.parse_args()
    
    ethical_scan(args.number)
    social_media_check(args.number)
    
    print("\n[!] Scan Complete - Delete results if unauthorized")

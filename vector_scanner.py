"""
Vector Scanner v1.0 - Ethical Digital Forensics Tool
Created by Victor - https://github.com/victor410fer
"""
import json
import requests
import argparse
from time import sleep
import webbrowser

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

def load_config():
    try:
        with open('config.json') as f:
            return json.load(f)
    except FileNotFoundError:
        print("[!] Missing config.json - Setup required")
        exit()

def ethical_scan(number):
    config = load_config()

    # Rate limiting
    sleep(5)
    # Numverify API call
    try:
        response = requests.get(
            f"http://apilayer.net/api/validate?access_key={config['NUMVERIFY_API_KEY']}&number={number}"
        )
        data = response.json()
        
        print("\n[+] Validated Information:")
        print(f"Number: {data.get('number')}")
        print(f"Valid: {data.get('valid')}")
        print(f"Country: {data.get('country_name')}")
        print(f"Carrier: {data.get('carrier')}")
        
    except requests.RequestException as e:
        print(f"API Error: {e}")

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

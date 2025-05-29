import pandas as pd
import requests
import re
import json
import pickle
import os

def fetch_data(country):
    """Fetch internet quality data for a given country from speedtest.net."""
    url = f'https://www.speedtest.net/global-index/{country}'
    response = requests.get(url)
    pattern = r'var data = (\{.*?\});'
    match = re.search(pattern, response.text, re.DOTALL)
    if match:
        json_str = match.group(1)
        data = json.loads(json_str)
        return data
    else:
        print(f"Dictionary not found in the HTML content for {country}.")
        return None

def merge_cis_data(new_data, old_data):
    merged_data = {}
    # Process all countries in the new data
    for country, new_country_data in new_data.items():
        merged_data[country] = new_country_data.copy()
        if country in old_data:
            old_country_data = old_data[country]
            for metric in ['fixedMean', 'mobileMean', 'fixedMedian', 'mobileMedian']:
                new_dates = set(item['date'] for item in new_country_data.get(metric, []))
                for old_item in old_country_data.get(metric, []):
                    if old_item['date'] not in new_dates:
                        merged_data[country][metric].append(old_item)
                merged_data[country][metric].sort(key=lambda x: x['date'])
    # Add countries that only exist in the old data
    for country, old_country_data in old_data.items():
        if country not in merged_data:
            merged_data[country] = old_country_data
    return merged_data

from datetime import datetime, timezone, timedelta

def main():
    cis_pickle_path = os.path.join(os.path.dirname(__file__), 'cis_new')
    # --- Date check logic ---
    now = datetime(2025, 5, 29, 15, 47, 39, tzinfo=timezone(timedelta(hours=4)))  # Use system-provided current time
    if os.path.exists(cis_pickle_path):
        mtime = os.path.getmtime(cis_pickle_path)
        last_modified = datetime.fromtimestamp(mtime, tz=timezone(timedelta(hours=4)))
        # If last modified is in the same year and month as now, skip update
        if last_modified.year == now.year and last_modified.month == now.month:
            print(f"cis_new was already updated this month on {last_modified.strftime('%Y-%m-%d')}. Skipping update.")
            return
    # Load existing data
    if os.path.exists(cis_pickle_path):
        with open(cis_pickle_path, 'rb') as f:
            cis_data_old = pickle.load(f)
    else:
        cis_data_old = {}
    # List of CIS countries
    cis_countries = [
        'armenia', 'azerbaijan', 'belarus', 'kazakhstan', 'kyrgyzstan',
        'moldova', 'russia', 'tajikistan', 'uzbekistan'
    ]
    # Fetch new data
    cis_data_new = {}
    for country in cis_countries:
        data = fetch_data(country)
        if data:
            cis_data_new[country] = data
    # Merge and deduplicate
    merged_cis_data = merge_cis_data(cis_data_new, cis_data_old)
    # Save merged data
    with open(cis_pickle_path, 'wb') as f:
        pickle.dump(merged_cis_data, f)
    print('CIS data updated and saved to cis_new.')

if __name__ == '__main__':
    main()

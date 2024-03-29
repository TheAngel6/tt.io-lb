import os
import requests
from bs4 import BeautifulSoup
import json

# Retrieve the Discord webhook URL from the environment variable
webhook_url = os.getenv('WEBHOOK_URL')

# Function to scrape top 30 clans from territorial.io
def scrape_top_clans():
    try:
        response = requests.get('https://territorial.io/clans')
        soup = BeautifulSoup(response.content, 'html.parser')
        content = response.text
        lines = content.split('\n')
        top_30_clans = []
        for line in lines:
            parts = line.split(',')
            if len(parts) == 3 and parts[0].strip().isdigit():
                rank = parts[0].strip()
                name = parts[1].strip()
                points = parts[2].strip()
                if name and points.replace('.', '').isdigit():
                    clan_info = f'{rank}. {name} - Points: {points}'
                    top_30_clans.append(clan_info)
        return top_30_clans[:30]
    except Exception as e:
        return None

# Function to send data to Discord using webhook
def send_to_discord(clans, custom_message=None):
    try:
        payload = {'content': '\n'.join(clans)}
        if custom_message:
            payload['content'] = custom_message + '\n' + payload['content']
        requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    except Exception as e:
        print("Error sending data to Discord:", e)

# Scrape top 30 clans from territorial.io
top_30_clans = scrape_top_clans()

# Custom message
if top_30_clans:
    custom_message = "# Here are the top clans presented by CTV <:ctv:1167501777898328064>"
    send_to_discord(top_30_clans, custom_message)

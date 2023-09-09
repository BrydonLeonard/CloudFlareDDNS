import json
import requests
import sqlite3
import time

import my_secrets


DB_NAME = "dns.db"


def get_db_connection():
    return sqlite3.connect(DB_NAME)

def configure_db():
    statement = """
        create table if not exists ip(
            v4address text not null,
            first_cached long not null
        )
    """

    con = get_db_connection()
    con.execute(statement)
    con.close()

def get_public_ip():
    response = requests.request(
                'GET',
                'https://api.ipify.org',
            )

    if (response.ok):
        return response.text
    else:
        print("Failed to get IP")
        return None
    

def update_cloudflare_records(ip):
    response = requests.request(
        'PUT',
        f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records/{CLOUDFLARE_RECORD_ID}",
        headers = {
            'X-Auth-Email': CLOUDFLARE_EMAIL,
            'X-Auth-Key': CLOUDFLARE_TOKEN
        },
        data = json.dumps({
            'content': ip,
            'name': DNS_ADDRESS,
            'proxied': True,
            'type': 'A',
            'comment': "Dynamic update at {time.time}",
            'ttl': 60
        })
    )

    if (response.ok):
        print("Successfully updated CloudFlare DNS entry")
    else: 
        print("Failed to update CLoudFlare DNS entry:" + response.text)
    
def get_latest_cached_ip():
    query = """
        select v4address from ip 
        order by first_cached desc
        limit 1
    """

    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    con.close()

    if len(results) == 0:
        return None
    else:
        return results[0][0]
    
def cache_ip(ip):
    statement = """
        insert into ip(v4address, first_cached)
        values (?,?)
    """

    con = get_db_connection()
    con.execute(statement, (ip, round(time.time())))
    con.commit()
    con.close()


def monitor_ip():
    active_ip = get_public_ip()
    cached_ip = get_latest_cached_ip()

    print(f"Active/Cached IP - {active_ip}/{cached_ip}")

    if (active_ip != cached_ip):
        update_cloudflare_records(active_ip)
        cache_ip(active_ip)

print("Running")

if __name__ == "__main__":
    print("Configuring DB")
    configure_db()

    print("Poll starting")
    while (True):
        print("Polling")
        monitor_ip()
        time.sleep(5)
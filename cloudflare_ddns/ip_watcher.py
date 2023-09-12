import requests

class IpWatcher:
    def __init__(self, db, cloudflare_client):
        self.db = db
        self.cloudflare_client = cloudflare_client

    def get_public_ip(self):
        response = requests.request(
                    'GET',
                    'https://api.ipify.org',
                )

        if (response.ok):
            return response.text
        else:
            raise Exception("Failed to get IP")

    def monitor_ip(self):
        active_ip = self.get_public_ip()
        cached_ip = self.db.get_latest_cached_ip()

        if (active_ip != cached_ip):

            print(f"IP changed from {cached_ip} to {active_ip}")
            self.cloudflare_client.update_cloudflare_records(active_ip)
            self.db.cache_ip(active_ip)
import json, requests

class CloudFlareClient:
    def __init__(self, config, db):
        self.email_address = config["EMAIL_ADDRESS"]
        self.api_key = config["API_KEY"]
        self.domain_name = config["DOMAIN_NAME"]

        # Doing all of this in the constructor is a little yucky, but the codebase is small enough that I don't really care
        cached_zone_id = db.get_zone_id(self.domain_name)
        if (cached_zone_id is not None):
            self.zone_id = cached_zone_id
        else:
            self.zone_id = self._get_zone_id()

        cached_record_id = db.get_record_id(self.domain_name)
        if (cached_record_id is not None):
            self.record_id = cached_record_id
        else:
            self.record_id = self._get_record_id()

        db.cache_record(self.record_id, self.domain_name, self.zone_id)
        
    def update_cloudflare_records(self, ip):
        response = requests.request(
            'PUT',
            f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records/{self.record_id}",
            headers = {
                'Content-Type': "application/json",
                'X-Auth-Email': self.email_address,
                'X-Auth-Key': self.api_key
            },
            data = json.dumps({
                'content': ip,
                'name': self.domain_name,
                'proxied': True,
                'type': 'A',
                'comment': "Dynamic update at {time.time}",
                'ttl': 60
            })
        )

        if (response.ok):
            print("Successfully updated CloudFlare DNS entry")
        else: 
            print("Failed to update CloudFlare DNS entry:" + response.text)

    # Private #

    def _get_zone_id(self):
        """
        https://developers.cloudflare.com/api/operations/zones-get
        """
        response = requests.request(
            'GET',
            f"https://api.cloudflare.com/client/v4/zones",
            headers = {
                'Content-Type': "application/json",
                'X-Auth-Email': self.email_address,
                'X-Auth-Key': self.api_key
            },
            data = json.dumps({
                'name': self.domain_name
            })
        )

        if (response.ok):
            response_json = json.loads(response.text)

            try:
                return response_json["result"][0]["id"]
            except:
                raise Exception("Failed to parse: " + response.text)
        else: 
            raise Exception("Failed to retrieve zone ID:" + response.text)

    def _get_record_id(self):
        """
        https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-list-dns-records
        """
        response = requests.request(
            'GET',
            f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records",
            headers = {
                'Content-Type': "application/json",
                'X-Auth-Email': self.email_address,
                'X-Auth-Key': self.api_key
            },
            data = json.dumps({
                'name': self.domain_name
            })
        )

        if (response.ok):
            response_json = json.loads(response.text)

            try:
                return response_json["result"][0]["id"]
            except:
                raise Exception("Failed to parse: " + response.text)
        else: 
            raise Exception("Failed to retrieve record ID:" + response.text)
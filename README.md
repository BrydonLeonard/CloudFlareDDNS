# CloudFlare DDNS

A little script for dynamic DNS on CloudFlare. You should probably use something like [DDClient](https://github.com/ddclient/ddclient) or [DNS-O-Matic](https://dnsomatic.com/docs/), but I built this for fun.

## Usage

1. Clone the repo and run `pip install .`
2. Head to [the CloudFlare dashboard](https://dash.cloudflare.com/) and grab:
   1. The domain name of the record you want to update
   2. Your global API key
   3. The email address associated with your CloudFlare account
3. Set all the required environment variables:
```
export CDDNS_API_KEY="Your API key"
export CDDNS_DOMAIN_NAME="Your domain name"
export CDDNS_EMAIL_ADDRESS="Your email address
export CDDNS_DB_PATH="The path where you'd like the SQLite DB saved"
```
4. Run `python3 cloudflare_ddns.py`
5. ???
6. Profit


## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
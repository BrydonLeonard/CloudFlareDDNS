import logging, os, time

from cloudflare_ddns.cloudflare_client import CloudFlareClient 
from cloudflare_ddns.db import DB
from cloudflare_ddns.ip_watcher import IpWatcher

def read_env_var_config():
    return {
        "API_KEY": os.getenv('CDDNS_API_KEY'),
        "DOMAIN_NAME": os.getenv('CDDNS_DOMAIN_NAME'),
        "EMAIL_ADDRESS": os.getenv('CDDNS_EMAIL_ADDRESS'),
        "DB_PATH": os.getenv("CDDNS_DB_PATH"),
        "LOG_PATH": os.getenv("CDDNS_LOG_PATH")
    }


if __name__ == "__main__":
    logging.info("Logging config")
    config = read_env_var_config()
    if (config["LOG_PATH"] is not None):
        logging.basicConfig(filename=config["LOG_PATH"], level=logging.DEBUG)
    try:
        logging.info("Starting")
        db = DB(config["DB_PATH"])
        cloudflare_client = CloudFlareClient(config, db)
        ip_watcher = IpWatcher(db, cloudflare_client)

        while (True):
            try:
                ip_watcher.monitor_ip()
            except: 
                logging.exception("Failed to monitor IP")
            time.sleep(5)
    except:
        logging.exception(f"Failed to start up")
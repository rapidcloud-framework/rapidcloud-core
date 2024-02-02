#!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import os
import subprocess
import traceback
from datetime import datetime

import public_ip as ip
from commands import general_utils
from commands.colors import colors


def activate_amazon_linux_ec2(email, lic_worker):
    domain = email.split('@')[1].split('.')[0]
    subdomain = f"{domain}.rapid-cloud.io".lower()

    print(f"\nAmazon Linux hosted RapidCloud requires SSL certificate and {subdomain} subdomain to provide secure access to RapidCloud Web Console.")
    print(f"\n{colors.WARNING}Make sure to confirm your email before proceeding!{colors.ENDC}\n")

    activation = general_utils.load_json_file('config/activation.json')
    subdomain = create_nginx_conf(subdomain)
    activation["create_nginx_conf"] = str(datetime.now())
    create_subdomain(subdomain, lic_worker)
    activation["create_subdomain"] = str(datetime.now())
    run_certbot(subdomain)
    activation["run_certbot"] = str(datetime.now())
    with open('config/activation.json', 'w') as f:
        json.dump(activation, f, indent=2)


def create_nginx_conf(subdomain):
    cwd = os.getcwd()
    cmd = f"sudo {cwd}/scripts/amazon_linux_config.sh {subdomain}"
    print(f"\nsubdomain: {subdomain}")
    print(f"cwd: {cwd}")
    print("\nFollowing command creates initial configuration for nginx:")
    print(f"\n{cmd}\n")
    proc = subprocess.run(cmd, shell=True, check=True, env=os.environ.copy(), cwd=cwd)
    return subdomain


def create_subdomain(subdomain, lic_worker):
    try:
        public_ip = ip.get()
        # response = requests.get("http://169.254.169.254/latest/dynamic/instance-identity/document", timeout=1)
        # instance_id = json.loads(response.text)["instanceId"]
        # resp = boto_session.client("ec2").describe_instances(InstanceIds=[instance_id])
        # public_ip = resp["Reservations"][0]["Instances"][0]["PublicIpAddress"]
        print(f"\nCreating or updating subdomain {subdomain} -> Public IP Address: {public_ip}")
        params = {
            "subdomain": subdomain,
            "public_ip": public_ip
        }
        lic_worker.create_subdomain(params)

    except Exception as e:
        print(e)
        traceback.print_exc()


def run_certbot(subdomain):
    try:
        public_ip = ip.get()
        cmd = f"echo -n 'waiting 300 seconds for dns records to update' ; timeout --foreground 120 bash -c 'while [[ $(dig +short {subdomain}) != {public_ip} ]] ; do sleep 5; echo . ; done'"
        print(cmd)
        proc = subprocess.run(cmd, shell=True, check=True, env=os.environ.copy(), cwd=os.getcwd())
        # sudo certbot --nginx -d <subdomain>.rapid-cloud.io
        print(f"\nRunning certbot to generate SSL certificate:\n")
        cmd = f"sudo certbot --nginx -d {subdomain} --non-interactive --agree-tos -m admin@rapid-cloud.io"
        print(cmd)
        proc = subprocess.run(cmd, shell=True, check=True, env=os.environ.copy(), cwd=os.getcwd())
    except Exception as e:
        print(e)

    try:
        filename = f"/etc/nginx/conf.d/{subdomain}.conf"
        # add forward to port 5000 after this line:
        with open(filename, 'r') as file:
            data = file.read()
            if "proxy_pass http://localhost:5000;" not in data:
                # listen 443 ssl; # managed by Certbot
                #
                # location / { # added by RapidCloud
                #     proxy_pass http://localhost:5000; # added by RapidCloud
                # } # added by RapidCloud
                print(f"\nAdding forward from port 443 to 5000:\n")
                for cmd in [
                    "sudo sed -i \"/listen 443 ssl; # managed by Certbot/a\ \ \ \ location \/ { # added by RapidCloud\"",
                    "sudo sed -i \"/location \/ { # added by RapidCloud/a\ \ \ \ \ \ \ \ proxy_pass http:\/\/localhost:5000; # added by RapidCloud\"",
                    "sudo sed -i \"/proxy_pass http:\/\/localhost:5000; # added by RapidCloud/a\ \ \ \ } # added by RapidCloud\""
                ]:
                    cmd = cmd + " " + filename
                    print(cmd)
                    proc = subprocess.run(cmd, shell=True, check=True, env=os.environ.copy(), cwd=os.getcwd())
    except Exception as e:
        print(e)


def renew_cert(subdomain, boto_session):
    print(f"\nYour SSL certificate will auto-renew every 3 months. Scheduling auto-renewal via cron job ...")
    pass

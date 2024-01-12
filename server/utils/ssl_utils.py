#!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

from datetime import datetime
import os
import subprocess

def check_certbot_renewal(activation_info):
    curr_ymd = int(datetime.today().strftime('%Y%m%d'))
    if os.path.exists("certbot.txt"):
        last_ymd = int(open("certbot.txt","r").read())
    else:
        last_ymd = 0
    if curr_ymd > last_ymd and "email" in activation_info:
        print("Checking for SSL cert renewal ...")
        certbot_renew_check_file = open("certbot.txt", "w")
        certbot_renew_check_file.write(str(curr_ymd))
        certbot_renew_check_file.close()
        try:
            cmd = f"sudo certbot renew --quiet --nginx"
            print(f"\t{cmd}")
            proc = subprocess.run(cmd, shell=True, check=True, env=os.environ.copy(), cwd=os.getcwd())
        except Exception as e:
            print(e)

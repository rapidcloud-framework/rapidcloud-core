#!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import logging
import traceback
from six.moves.urllib.request import urlopen, Request
from jose import jwt
import certifi

from server.utils.server_helper import ServerHelper


AUTH0_DOMAIN_DEV = "rapidcloud-dev.us.auth0.com"
AUTH0_DOMAIN_LIVE = "rapidcloud.us.auth0.com"
API_AUDIENCE = "https://rapid-cloud.io"
ALGORITHMS = ["RS256"]

class AuthHelper(ServerHelper):

    logger = logging.getLogger(__name__)

    def __init__(self, args, app_mode):
        super().__init__(args, app_mode)
        self.args = args


    def get_user_info(self, request):
        try:
            # self.logger.info(f"request.headers:\n{request.headers}")
            auth = request.headers.get('Authorization')
            if auth:
                token = auth.split()[1]
            else:
                self.logger.error("Authorization header not found")
                return None

            AUTH0_DOMAIN = AUTH0_DOMAIN_LIVE if self.app_mode == "live" else AUTH0_DOMAIN_DEV
            # self.logger.info(certifi.where())
            jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
            jwks = json.loads(jsonurl.read())
            # self.logger.info(f"\n\njwks: \n{json.dumps(jwks, indent=2, default=str)}")
            unverified_header = jwt.get_unverified_header(token)
            # self.logger.info(f"\n\nunverified_header: \n{json.dumps(unverified_header, indent=2, default=str)}")

            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }

            # self.logger.info(f"\n\nrsa_key: \n{json.dumps(rsa_key, indent=2, default=str)}")
            if rsa_key:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer=f"https://{AUTH0_DOMAIN}/"
                )
                # self.logger.info(f"\n\npayload: \n{json.dumps(payload, indent=2, default=str)}")

                request = Request(f"https://{AUTH0_DOMAIN}/userinfo")
                request.add_header("Authorization", f"Bearer {token}")
                data = urlopen(request).read().decode()
                user_info = json.loads(data)
                return user_info
            else:
                self.logger.warning("rsa_key not found")
                return None

        except Exception as e:
            traceback.print_exc()
            return None

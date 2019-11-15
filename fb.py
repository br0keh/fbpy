import requests
import hashlib
import json


class Facebook:
    def __init__(self, email, password, proxy):
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.session.proxies = {'https': 'https://%s' % proxy}

    def generate_sig(self, payload):
        sig = ""

        for key, value in payload.items():
            sig = sig + "%s=%s;" % (key, value)

        sig = hashlib.md5(sig.encode()).hexdigest()

        return sig

    def login(self):
        email = self.email
        password = self.password
        session = self.session

        headers = {
            'User-agent': 'Opera/9.80 (Series 60; Opera Mini/7.0.32400/28.3445; U; en) Presto/2.8.119 Version/11.10'}

        payload = {
            "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
            "email": email,
            "password": password,
            "locale": "en_US",
            "format": "JSON"
        }

        payload['sig'] = self.generate_sig(payload)

        auth_request = False

        try:
            auth_request = session.post('https://api.facebook.com/method/auth.login',
                                        data=payload, headers=headers, timeout=20)
        except Exception as ex:
            proxy_errors = ['InvalidURL', 'ConnectTimeout', 'ProxyError']
            for proxy_error in proxy_errors:
                if proxy_error in type(ex).__name__:
                    if 'ProxyError' in proxy_error:
                        return {
                            'error': 'Proxy Error'
                        }
                    return {'error': 'Proxy Error (PROXY-%s)' % (proxy_error)}

        if not auth_request:
            return {
                'error': "IP Banned"
            }

        response = json.loads(auth_request.content)

        if 'error_code' in response:

            if 'Calls to this api have exceeded the rate limit' in response['error_msg']:
                return {
                    'error': "IP Banned"
                }
            elif 'User must confirm their e-mail address on www.facebook.com' in response['error_msg']:
                return {
                    'error': 'Need to confirm e-mail address.'
                }

            return {
                'error': response['error_msg']
            }

        elif 'session_key' in response:
            return {
                'success': response
            }

        else:
            return {
                'error': 'Unknow'
            }
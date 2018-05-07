import json
import time
import requests

from hashlib import md5

ADD_ENDPOINT = "https://incandescent.xyz/api/add/"
GET_ENDPOINT = "https://incandescent.xyz/api/get/"

UID = 7429
API_KEY = "d35ea63babe3b47fbced5046e330fccd"

WAIT_TIME = 10


class Client(object):
    def __init__(self):
        self.data = {}

        self.image_urls = None
        self.project_id = None

    def add_image_urls(self, image_urls):
        self.image_urls = image_urls
        self.data['images'] = self.image_urls

    def make_request_data(self):
        expires_seconds = int(time.time())
        expires_seconds = expires_seconds + 1000
        string_to_sign = str(UID) + "-" + str(expires_seconds) + "-" + API_KEY
        auth = md5(string_to_sign.encode('utf-8')).hexdigest()
        self.data['uid'] = UID
        self.data['expires'] = expires_seconds
        self.data['auth'] = auth

    def make_request(self):
        try:
            r = requests.post(ADD_ENDPOINT, json=self.data)
            if r.status_code == 200:
                response = json.loads(r.content)
                if 'project_id' in response:
                    project_id = response['project_id']
                    self.project_id = project_id
                    self.data['images'] = None
                elif 'error' in response:
                    self.project_id = None
        except Exception as e:
            print(e)
            self.project_id = None

    def get_results(self):
        try:
            self.data['project_id'] = self.project_id
            r = requests.post(GET_ENDPOINT, json=self.data)
            response = json.loads(r.content)
            if response.get('status') == 710:
                time.sleep(WAIT_TIME)
                return self.get_results()
            results = []
            if 'status' not in response:
                for site, site_results in response.items():
                    for page, result in site_results.get('pages', {}).items():
                        if result.get('page'):
                            results.append(result.get('page'))
            return results
        except Exception as e:
            print(e)
            self.project_id = None
            return None

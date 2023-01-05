import datetime
import json
import logging
import requests


class ApiService:
    def __init__(self, headers=None):
        if headers is None:
            headers = {}
        self.header = {'content-type': 'application/json', **headers}

    def get(self, end_point, headers):
        try:
            response = requests.get(end_point, headers={**self.header, **headers})
            response = response.json()
            return response
        except requests.exceptions.RequestException:
            logging.warning('API failed to fetch results')

    def post(self, end_point, d):
        try:
            response = requests.post(end_point, data=d, headers=self.header)
            response = response.json()
            return response
        except requests.exceptions.RequestException:
            logging.warning('API failed to fetch results')

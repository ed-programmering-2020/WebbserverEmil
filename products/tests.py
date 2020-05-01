from rest_framework.test import APIClient
from django.test import TestCase
import requests
import json


class ScrapingTestCase(TestCase):
    def setUp(self):
        r = requests.post("http://127.0.0.1:8000/api/auth/login/",
                          data={"username": "test", "password": "test"})
        content = dict(json.loads(r.content))
        token = content["token"]

        items = [
            {'availability': 0,
             'campaign': True,
             'category': 'Laptop',
             'image_urls': ['//inetimg3.se/img/688x386/6903945_3.jpg'],
             'manufacturing_name': 'LAN2-3X',
             'name': 'Lian Li Lancool II Hot-Swap bakpanel',
             'price': 249,
             'rating': 0,
             'review_count': None,
             'shipping': 0,
             'specifications': {},
             'url': 'https://www.inet.se/produkt/6903945/lian-li-lancool-ii-hot-swap-bakpanel',
             "host": "inet",
             'used': False}
        ]
        items_json = json.dumps(items)
        r = requests.post("http://127.0.0.1:8000/api/scraping/products/",
                          data={"products": items_json},
                          headers={"Authorization": "Token " + token})
        print(r.status_code)


from rest_framework.test import APIClient
from users.models import User
from django.test import TestCase


class ScrapingTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="test", is_staff=True)
        self.client = APIClient()
        self.client.force_login(user)

        self.base_item = {
            "name": "test",
            "manufacturing_name": "test",
            "price": 1,
            "url": 'https://www.test.com',
            "guarantee": 1,
            "image_urls": ['//inetimg3.se/img/688x386/6903945_3.jpg'],

            "height": 1,
            "width": 1,
            "depth": 1,
            "weight": 1,

            "availability": 0,
            "campaign": True,
            "rating": 0,
            "review_count": None,
            "shipping": 0,
            "host": "inet",
            "used": False
        }

    def test_laptop_scraping(self):
        item = self.base_item
        item.update({
            "category": 'Laptop',

            "screen_size": 15.6,
            "resolution": 1080,
            "refresh_rate": 60,
            "panel_type": "retina",

            "storage_type": "ssd",
            "storage_size": 128,

            "processor": "core i5 8265u",
            "graphics_card": "geforce mx250",

            "ram_capacity": 8,
            "battery_time": 8,
            "color": "svart",
            "operating_system": "windows 10"
        })

        r = self.client.post("/scraping/products", {"products": [item]})
        self.assertNotEqual(r.status_code, 500)

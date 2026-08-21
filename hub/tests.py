from django.test import TestCase
from django.urls import reverse


class HubHomeTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('hub:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Scanner para Excel')

# Create your tests here.

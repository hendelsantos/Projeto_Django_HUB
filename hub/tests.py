from django.test import TestCase
from django.urls import reverse


class HubHomeTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('hub:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Scanner para Excel')
        self.assertContains(response, 'PhotoCloud')

    def test_photocloud_page_loads(self):
        response = self.client.get(reverse('hub:photocloud'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PhotoCloud')
        self.assertContains(response, 'https://photo-cloud-1.onrender.com/')
        self.assertContains(response, '10 minutos')

    def test_photocloud_qrcode_loads(self):
        response = self.client.get(reverse('hub:photocloud_qrcode'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')

# Create your tests here.

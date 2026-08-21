from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class HubHomeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='operador',
            password='senha-teste-123',
        )

    def test_home_page_hides_photocloud_for_anonymous_user(self):
        response = self.client.get(reverse('hub:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Scanner para Excel')
        self.assertNotContains(response, 'PhotoCloud')

    def test_home_page_shows_photocloud_for_logged_user(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('hub:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PhotoCloud')

    def test_photocloud_page_redirects_anonymous_user(self):
        response = self.client.get(reverse('hub:photocloud'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response['Location'])

    def test_photocloud_page_loads_for_logged_user(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('hub:photocloud'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PhotoCloud')
        self.assertContains(response, 'https://photo-cloud-1.onrender.com/')
        self.assertContains(response, '10 minutos')

    def test_photocloud_qrcode_redirects_anonymous_user(self):
        response = self.client.get(reverse('hub:photocloud_qrcode'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response['Location'])

    def test_photocloud_qrcode_loads_for_logged_user(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('hub:photocloud_qrcode'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')

# Create your tests here.

from django.test import TestCase
from django.urls import reverse


class GatewayFlowTests(TestCase):
    def test_login_generates_pending_user_and_code(self):
        response = self.client.post(
            reverse('login'),
            {
                'name': 'Demo User',
                'email': 'demo@example.com',
                'phone': '+52 555 123 4567',
            },
        )

        self.assertRedirects(response, reverse('verify'))
        session = self.client.session
        self.assertIn('pending_user', session)
        self.assertEqual(len(session['pending_user']['code']), 6)

    def test_correct_code_reaches_redirecting_page(self):
        self.client.post(
            reverse('login'),
            {
                'name': 'Demo User',
                'email': 'demo@example.com',
                'phone': '+52 555 123 4567',
            },
        )
        code = self.client.session['pending_user']['code']

        response = self.client.post(reverse('verify'), {'code': code})

        self.assertRedirects(response, reverse('redirecting'))
        self.assertIn('verified_user', self.client.session)

    def test_redirecting_requires_verification(self):
        response = self.client.get(reverse('redirecting'))

        self.assertRedirects(response, reverse('login'))

# Create your tests here.

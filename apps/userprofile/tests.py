from django.core.urlresolvers import reverse
from django.test import TestCase


class UserProfileTestCase(TestCase):
    def setUp(self):
        pass
        # UserProfile.objects.create(user_id=2, account_type="1", display_name='Chaka Chaka')

    def test_login_200(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_profile_anonymous_redirect(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    # def test_profile_logged_200(self):
    #     User.objects.create(username='test', password='test', is_active=True, email='aas@asf.com')
    #     user = authenticate(username='test', password='test')
    #     login(self.request, user)
    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(response.status_code, 200)

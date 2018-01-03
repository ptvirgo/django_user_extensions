from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import get_current_timezone_name
from django.contrib.auth import get_user_model
from ..models import ExtendedUserProfile


class TestTimezone(TestCase):

    @classmethod
    def setUpClass(cls, *args, **kwargs):

        super().setUpClass(*args, **kwargs)

        UserModel = get_user_model()
        user = UserModel(first_name='Test', last_name='User',
                         username='tuser-timezones')
        user.set_password('thisisatest123')
        user.save()

        profile = ExtendedUserProfile(user=user, country='US',
                                      timezone='America/Metlakatla')
        profile.save()

        cls.authorized_client = Client()

        logged_in = cls.authorized_client.login(
            username=user.username, password='thisisatest123')

        if not logged_in:
            raise RuntimeError('Could not log in to test server')

    def test_timezone_at_login(self):
        '''When a user logs in, the timezone should be set.'''

        self.authorized_client.get(reverse('profile'))
        self.assertEqual(get_current_timezone_name(), 'America/Metlakatla')

    def test_timezone_changes(self):
        '''When the user saves a new timezone, it should be set.'''

        response = self.authorized_client.post(
            reverse('profile'),
            {'country': 'NZ', 'timezone': 'Pacific/Auckland'})

        self.assertEqual(response.status_code, 201)

        self.assertEqual(get_current_timezone_name(), 'Pacific/Auckland')

        response = self.authorized_client.post(
            reverse('profile'),
            {'country': 'US', 'timezone': 'America/Metlakatla'})

        self.assertEqual(get_current_timezone_name(), 'America/Metlakatla')

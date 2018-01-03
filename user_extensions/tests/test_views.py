from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import ExtendedUserProfile


class TestRegistrationView(TestCase):
    client = Client()

    @classmethod
    def setUpClass(cls, *args, **kwargs):

        super().setUpClass(*args, **kwargs)

        UserModel = get_user_model()
        user = UserModel(first_name='Test', last_name='User',
                         username='tuser-registration')
        user.set_password('thisisatest123')
        user.save()

        authorized_client = Client()

        logged_in = authorized_client.login(
            username=user.username, password='thisisatest123')

        if not logged_in:
            raise RuntimeError('Could not log in to test server')

        cls.authorized_client = authorized_client
        
    def test_registration_display(self):
        '''Registration form displays properly'''

        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Username')
        self.assertContains(response, 'Email')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'Captcha')

    def test_registration_of_user(self):
        '''Registration creates a user'''

        response=self.client.post(
            reverse('register'),
                    {'username': 'Larry', 'email': 'larry@testing.com',
                     'password1': 'theultimate',
                     'password2': 'theultimate',
                     'g-recaptcha-response': 'testing'})

        UserModel = get_user_model()

        user = UserModel.objects.get(username='Larry',
                                     email='larry@testing.com')

    def test_profile_requires_login(self):
        '''Profile view without login should redirect'''
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_view(self):
        '''Profile view should display correct fields and
        default values
        '''

        response = self.authorized_client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Country')
        self.assertContains(response, 'Timezone')
        self.assertContains(response, 'US/Eastern')

    def test_profile_change(self):
        '''Editing a profile should show changes'''
                
        response = self.authorized_client.post(
            reverse('profile'),
            {'country': 'NZ', 'timezone': 'Pacific/Auckland'})

        self.assertContains(response, 'NZ', status_code=201)
        self.assertContains(response, 'Pacific/Auckland', status_code=201)

        response = self.authorized_client.post(
            reverse('profile'),
            {'country': 'US', 'timezone': 'US/Eastern'})

        self.assertEqual(response.status_code, 201)

    def test_profile_errors(self):
        '''Editing a profile with invalid data should fail.'''

        response = self.authorized_client.post(
            reverse('profile'), {'country': 'LA'})

        self.assertContains(response, 'errorlist', status_code=400)

        response = self.authorized_client.post(
            reverse('profile'), {'timezone': 'Lemon'})

        self.assertContains(response, 'errorlist', status_code=400)

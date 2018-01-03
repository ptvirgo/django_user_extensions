from django.test import TestCase
from django.core.exceptions import ValidationError
from .. import validators


class TestValidators(TestCase):
    '''Test django model validators'''

    def test_country_codes(self):
        '''Country codes should be accurate'''

        self.assertEqual(validators.country_code('us'), 'US',
                         msg='recognizes us')
        self.assertRaises(ValidationError, validators.country_code, 'rr')

    def test_timezone(self):
        '''Time zones are validated'''

        self.assertEqual(validators.timezone('America/New_York'),
                         'America/New_York')
        self.assertRaises(ValidationError, validators.timezone, 'Forgot')

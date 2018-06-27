import pytz

from django.db import models
from django.conf import settings

from . import validators

countries = sorted(
    [(c, pytz.country_names[c]) for c in pytz.country_names],
    key=lambda x: x[1])

timezones = [(t, t) for t in pytz.all_timezones]


class ExtendedUserProfile(models.Model):
    '''Time zone and other standardized details here.'''

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    country = models.CharField(max_length=2,
                               validators=[validators.country_code],
                               choices=countries,
                               default='US')

    timezone = models.CharField(max_length=32,
                                validators=[validators.timezone],
                                choices=timezones,
                                default='US/Eastern')

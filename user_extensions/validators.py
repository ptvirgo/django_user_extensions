import pytz
from django.core.exceptions import ValidationError

def country_code(code):
    if code.upper() in pytz.country_timezones.keys():
        return code.upper()

    raise ValidationError('No such country code %s in pytz')

def timezone(zone):

    try:
        return str(pytz.timezone(zone))
    except pytz.exceptions.UnknownTimeZoneError as err:
        raise ValidationError('No such time zone %s it pytz')

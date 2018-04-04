import datetime

from jose import jwt

from django.conf import settings


def add_jwt(request):
    '''Add user's jwt to response context, if available.'''
    user = request.user

    if user is None or not user.is_authenticated:
        return {}

    now = datetime.datetime.now()
    timeout = now + settings.USER_EXTENSIONS['JWT_TIMEOUT']
    claim = {'exp': timeout.timestamp(),
             'nbf': now.timestamp(),
             'sub': user.pk}

    token = jwt.encode(
        claim, settings.SECRET_KEY, settings.USER_EXTENSIONS['JWT_ALGORITHM'])

    return {'jwt': token}

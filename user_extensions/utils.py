import datetime
from jose import jwt

from django.conf import settings

def user_jwt(user):

    if user is None or not user.is_authenticated:
        return

    now = datetime.datetime.now()
    timeout = now + settings.USER_EXTENSIONS['JWT_TIMEOUT']
    claim = {'exp': timeout.timestamp(),
             'nbf': now.timestamp(),
             'sub': str(user.pk)}

    token = jwt.encode(
        claim, settings.SECRET_KEY, settings.USER_EXTENSIONS['JWT_ALGORITHM'])

    return token
    

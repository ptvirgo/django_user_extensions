import datetime
from jose import jwt
import requests

from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def user_jwt(user):
    """Get a JWT for the User"""
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
    

def jwt_user(token):
    """Get a User from the JWT"""

    claims = jwt.decode(
        token, settings.SECRET_KEY,
        [getattr(settings, "JWT_ALGORITHM", "HS256")])

    try:
        user = User.objects.get(pk=int(claims["sub"]))
    except:
        raise ValueError("invalid token")

    return user


def recaptcha_passed(captcha, ip=None):
    """True if the given reCaptcha token validates via the google service"""

    params = { "secret": settings.RECAPTCHA_PRIVATE_KEY, "response": captcha }

    if ip is not None:
        params["remoteip"] = ip

    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data=params)

    jsr = response.json()
    return jsr["success"] is True

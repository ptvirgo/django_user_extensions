import requests
import graphene
from graphene_django import DjangoObjectType

from django.contrib.auth import authenticate
from django.conf import settings 

from . import utils


class JWTQuery(graphene.ObjectType):
    """JWT lookups"""

    new_jwt = graphene.String(
        username=graphene.String(required=True),
        password=graphene.String(required=True), 
        captcha=graphene.String(required=True)
    )

    refresh_jwt = graphene.String(token=graphene.String(required=True))

    def resolve_new_jwt(self, info, username, password, captcha, **kwargs):
        """Provide the new JWT"""

        if not utils.recaptcha_passed(captcha):
            raise ValueError("Failed reCaptcha")

        user = authenticate(username=username, password=password)

        if user is None:
            raise ValueError("Invalid Login")

        token = utils.user_jwt(user)
        return token        


    def resolve_refresh_jwt(self, info, token, **kwargs):
        """Provide a refreshed JWT"""

        user = utils.jwt_user(token)
        token = utils.user_jwt(user)
        return token

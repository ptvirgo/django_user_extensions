import json
from django.test import Client, TestCase

from ..utils import jwt_user
from ..factories import UserFactory


class GrapheneTestCase(TestCase):
    """Provide some standard test configuration for Graphql Queries"""

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        """Prepare a JWT for a valid test user"""

        super().setUpClass(*args, **kwargs)

        user = UserFactory()
        user.set_password("logmein")
        user.save()
        cls.user = user

    @staticmethod
    def execute(query, raise_errors=True):
        """Post a GQL query.
        Parameters
            raise_errors -- if True, response errors will be raised as
                            AssertionError
        """

        client = Client()
        response = client.post("/graphql/", {"query": query})
        text = response.content.decode("utf-8")

        try:
            result = json.loads(text)
        except Exception as err:
            raise err

        if raise_errors and "errors" in result:
            message = "Query Errors:\n    " + "\n   ".join(
                [error.get("message", "missing error message")
                 for error in result["errors"]])

            raise AssertionError(message)

        return result

class TestGQLJWT(GrapheneTestCase):
    """JWT can be retrieved as with a user login"""

    def test_get_jwt(self):
        """
        A user can get a jwt with username, password, and google recaptcha
        token
        """ 

        query = """
            { newJwt(username: "%s", password: "%s", captcha: "%s") }
            """ % (self.user.username, "logmein", "autosuccessontest")

        result = self.execute(query)

        self.assertEqual(jwt_user(result["data"]["newJwt"]), self.user)


    def test_refresh_jwt(self):
        """
        A user can refresh a jwt from a previous jwt
        """
        query = """
            { newJwt(username: "%s", password: "%s", captcha: "%s") }
            """ % (self.user.username, "logmein", "autosuccessontest")

        result = self.execute(query)
        token = result["data"]["newJwt"]

        query = """
            { refreshJwt(token: "%s") }
            """ % (token,)

        result = self.execute(query)

        self.assertEqual(jwt_user(result["data"]["refreshJwt"]), self.user)

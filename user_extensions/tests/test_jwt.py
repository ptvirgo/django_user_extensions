from jose import jwt

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings


class TestJWT(TestCase):
    """JWT Tokens should be available via response context"""

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)

        User = get_user_model()
        user = User(username="testJWT", first_name="Test", last_name="JWT")
        user.set_password("logmeinKTHXBYE!")
        user.save()

        client = Client()
        logged_in = client.login(
            username=user.username, password="logmeinKTHXBYE!")

        if not logged_in:
            raise RuntimeError("Could not log in to test server")

        cls.user = user
        cls.authorized_client = client

    def test_anon_user_no_jwt(self):
        """Anonymous users should not get a JWT"""

        client = Client()
        response = client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertIs(response.context.get("jwt", None), None)
        self.assertNotContains(response, "jwt")


    def test_auth_user_has_jwt(self):
        """Authenticated users should have a jwt"""

        response = self.authorized_client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context.get("jwt", None)) > 5)
        self.assertContains(response, "jwt")

    def test_jwt_validates(self):
        """JWT better decode properly"""

        response = self.authorized_client.get(reverse("home"))
        token = response.context["jwt"]
        claim = jwt.decode(token, settings.SECRET_KEY,
                           [getattr(settings, "JWT_ALGORITHM", "HS256")])

        self.assertEqual(int(claim["sub"]), self.user.pk)

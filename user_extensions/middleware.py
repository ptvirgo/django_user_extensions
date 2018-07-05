import pytz
from django.utils import timezone


class TimezoneMiddleware(object):

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):
        """Set the user's timezone, if applicable."""

        response = self.get_response(request)

        if request.user.is_authenticated:
            profile = getattr(request.user, "extendeduserprofile", None)

            if profile:
                user_tz = getattr(profile, "timezone", None)

                if user_tz:
                    timezone.activate(pytz.timezone(user_tz))
                else:
                    timezone.deactivate()

        return response

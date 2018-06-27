from .utils import user_jwt


def add_jwt(request):
    '''Add user's jwt to response context, if available.'''
    token = user_jwt(request.user)

    if token is None:
        return {}

    return {'jwt': token}

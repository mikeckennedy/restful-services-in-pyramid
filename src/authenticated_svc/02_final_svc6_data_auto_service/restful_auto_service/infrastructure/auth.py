from pyramid.response import Response

from restful_auto_service.data.repository import Repository


def parse_api_key(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None, "You must specify an Authorization header."

    parts = auth_header.split(':')
    if len(parts) != 2 or parts[0].strip() != 'api-key':
        return None, "Invalid auth header"

    api_key = parts[1].strip()
    user = Repository.find_user_by_api_key(api_key)
    if not user:
        return None, "Invalid API Key, no user with this account."

    return user, None


def require_api_auth(func):
    def wrapped(request):
        user, error = parse_api_key(request)
        if error:
            return Response(status=403, body=error)

        request.api_user = user

        return func(request)

    return wrapped

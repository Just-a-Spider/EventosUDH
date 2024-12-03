import jwt
from channels.db import database_sync_to_async
from django.db import close_old_connections
from channels.sessions import CookieMiddleware, SessionMiddleware
from channels.auth import AuthMiddleware
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from .auth_classes import role_to_model

@database_sync_to_async
def get_user(scope):
    close_old_connections()
    headers = dict(scope['headers'])
    access_token = None

    if b'cookie' in headers:
        cookie_str = headers[b'cookie'].decode()
        cookies_dict = dict(item.split("=") for item in cookie_str.split("; "))
        access_token = cookies_dict.get('access_token')

    if not access_token:
        return AnonymousUser()
    
    try:
        # Decode the token to get the JSON payload
        decoded_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
        username = decoded_payload.get('username')
        user_model = role_to_model.get(decoded_payload.get('role'))
        if username:
            try:
                user = user_model.objects.get(username=username)
                scope['user'] = user
                return user
            except user_model.DoesNotExist:
                return AnonymousUser()
        else:
            return AnonymousUser()
    except jwt.ExpiredSignatureError:
        return AnonymousUser()
    except jwt.InvalidTokenError:
        return AnonymousUser()

class TokenAuthMiddleware(AuthMiddleware):
    async def resolve_scope(self, scope):
        scope['user']._wrapped = await get_user(scope)
        
def TokenAuthMiddlewareStack(inner):
    return CookieMiddleware(SessionMiddleware(TokenAuthMiddleware(inner)))
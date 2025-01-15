import jwt
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs

User = get_user_model()


@database_sync_to_async
def get_user_from_token(token: str):
    try:
        access_token = AccessToken(token)
        user_id = access_token["user_id"]
        return User.objects.get(id=user_id)
    except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])

        authorization_header = headers.get(b"authorization", None)
        token = None
        if authorization_header is not None:
            auth_str = authorization_header.decode("utf-8")
            if auth_str.lower().startswith("bearer "):
                token = auth_str.split(" ", 1)[1].strip()

        if not token:
            query_string = parse_qs(scope["query_string"].decode("utf8"))
            token_list = query_string.get("token", [])
            if token_list:
                token = token_list[0]

        if token:
            user = await get_user_from_token(token)
        else:
            user = AnonymousUser()

        scope["user"] = user

        return await super().__call__(scope, receive, send)

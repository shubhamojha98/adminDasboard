SAFE_URL_NAMES = ["login", "signup", "password_reset"]  # Add URLs that should be public
import jwt
from django.conf import settings
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve  # Helps with URL name resolution

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if resolve(request.path_info).url_name in SAFE_URL_NAMES:
            return None  # Skip auth check

        token = request.COOKIES.get("jwt_token")

        if not token:
            return redirect("login")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            request.user = payload["username"]
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return redirect("login")

        return None

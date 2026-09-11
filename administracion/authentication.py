import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from rest_framework.exceptions import AuthenticationFailed


class SupabaseUser:
    """Minimal user object for DRF that holds the Supabase user ID."""

    def __init__(self, user_id, payload=None):
        self.id = user_id
        self.pk = user_id
        self.is_authenticated = True
        self.payload = payload or {}

    def __str__(self):
        return self.id


class SupabaseJWTAuthentication(authentication.BaseAuthentication):
    """
    Authenticate requests by verifying the Supabase JWT access token
    against the project's JWKS endpoint (asymmetric signing keys).
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ', 1)[1]

        try:
            # Unverified decode to extract header (kid, alg) for JWKS lookup
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get('kid')
            alg = unverified_header.get('alg', 'RS256')
        except jwt.exceptions.PyJWTError:
            raise AuthenticationFailed('Token JWT mal formado.')

        # Fetch the JWKS from Supabase
        jwks_url = f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"
        try:
            jwks_client = jwt.PyJWKClient(jwks_url, cache_keys=True)
            signing_key = jwks_client.get_signing_key_from_jwt(token)
        except Exception:
            raise AuthenticationFailed('No se pudieron obtener las claves de verificación de Supabase.')

        # Verify and decode
        try:
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=[alg],
                audience='authenticated',
                options={
                    'verify_exp': True,
                    'verify_aud': True,
                },
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('El token ha expirado. Inicia sesión de nuevo.')
        except jwt.InvalidAudienceError:
            raise AuthenticationFailed('Token con audiencia inválida.')
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f'Token inválido: {e}')

        user_id = payload.get('sub')
        if not user_id:
            raise AuthenticationFailed('Token no contiene identificación de usuario (sub).')

        return (SupabaseUser(user_id, payload), token)

    def authenticate_header(self, request):
        return 'Bearer'

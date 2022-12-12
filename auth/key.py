from json import load

from jwcrypto.jws import InvalidJWSSignature
from orjson import loads

from responses.errors import InvalidToken
from settings import JWK_KEY_FILE

from jwcrypto.jwk import JWK
from jwcrypto.jwt import JWT


class Key:
    """ Cumulative class, that stores all reprs of key and helps to load it """
    jwk: JWK

    def load_key(self, key_path: str = None):
        """
            Loads key from jwk key file

            Args:
                key_path: Optional. Key path, if unspecified, loaded from JWK_KEY_FILE env
        """
        if key_path is None:
            key_path = JWK_KEY_FILE
        self.jwk = JWK(**load(open(key_path)))


def decrypt_token(token: str):
    """ Decrypts and verifies JWT token

    Args:
        token: serialized JWT

    Returns:
        Decrypted claims
    """
    try:
        jwt = JWT(key=key.jwk, jwt=token)
    except InvalidJWSSignature:
        raise InvalidToken
    return loads(jwt.claims)


key = Key()

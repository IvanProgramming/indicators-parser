from jwcrypto.jwk import JWK


def create_and_save_key(key_file_name="key.jwk"):
    """
        Generates new RSA key and stores it in file

    Args:
        key_file_name (str): save path for jwk key
    """
    key = JWK.generate(kty="RSA", size=2048)
    with open(key_file_name, "w+") as f:
        f.write(key.export())

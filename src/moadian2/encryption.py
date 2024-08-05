from datetime import datetime, timezone
from authlib.jose import JsonWebEncryption, JsonWebSignature


__date_format = "%Y-%m-%dT%H:%M:%SZ"
__signature_time = datetime.now(timezone.utc).strftime(__date_format)


def sign(payload, key, cert):
    headers = {
    "alg": "RS256",
    "x5c": [cert],
    "sigT": __signature_time,
    "typ": "jose",
    "crit": ["sigT"],
    "cty": "text/plain"
    }

    jws = JsonWebSignature()
    signed = jws.serialize_compact(headers, payload.encode(), key)
    return signed.decode()


def encrypt(payload, key):
    jwe = JsonWebEncryption()
    protected = {
        'alg': 'RSA-OAEP-256',
        'enc': 'A256GCM',
        #'kid': server_public_key_id
    }
    encrypted = jwe.serialize_compact(
        protected,
        payload,
        key
    )
    return encrypted

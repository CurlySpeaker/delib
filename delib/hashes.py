import hashlib
from delib.settings import SECRET_KEY


def sha256(data):
    byte_string = bytes(data + SECRET_KEY, 'utf-8')
    return hashlib.sha256(byte_string).hexdigest()

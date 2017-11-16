import hashlib
import hmac


def make_hash(value):

    MY_SECRET_KEY = b'T1F43cP0Rs821g'  # Ключ
    return hmac.new(key=MY_SECRET_KEY, msg=value.encode('utf-8'), digestmod=hashlib.sha224).hexdigest()
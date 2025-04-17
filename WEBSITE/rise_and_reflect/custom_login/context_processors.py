import hmac
import hashlib
from django.conf import settings

def intercom_user_hash(request):
    if request.user.is_authenticated and settings.INTERCOM_SECRET_KEY:
        message = str(request.user.id).encode('utf-8')
        secret = settings.INTERCOM_SECRET_KEY.encode('utf-8')
        user_hash = hmac.new(secret, message, digestmod=hashlib.sha256).hexdigest()
        return {'user_hash': user_hash}
    return {}

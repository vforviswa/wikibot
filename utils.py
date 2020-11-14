import hashlib
import hmac
from time import time


class SignatureVerifier:
    def __init__(self, signing_secret):
        self.signing_secret = signing_secret
    
    def is_valid_request(self, body, headers):
        if not headers:
            return False
        timestamp = headers.get('X-Slack-Request-Timestamp')
        request_signature = headers.get('X-Slack-Signature')
        return self.is_valid(body, timestamp, request_signature)
    
    def is_valid(self, body, timestamp, request_signature):
        if None in (timestamp, request_signature):
            return False
        
        if abs(time() - int(timestamp)) > 60 * 5:
            return False
        
        my_signature = self.generate_signature(timestamp, body)
        return hmac.compare_digest(my_signature, request_signature)

    def generate_signature(self, timestamp, body):
        if isinstance(body, bytes):
            body = body.decode("utf-8")
        signature_basestring =  str.encode(f'v0:{timestamp}:{body}')
        encoded_secret = str.encode(self.signing_secret)
        request_hash = hmac.new(encoded_secret, signature_basestring, hashlib.sha256).hexdigest()
        my_signature = f'v0={request_hash}'
        return my_signature

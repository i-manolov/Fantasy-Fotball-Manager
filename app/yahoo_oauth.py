import urlparse
import httplib2
import time
import json
import oauth2 as oauth

consumer_key = 'dj0yJmk9ZUNVYWFZcW9pRUhBJmQ9WVdrOVZYQnVjbFo2TjJrbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD02ZA--'
consumer_secret = '91096b3d5dfa2045ead373faba062aa6c23c4e23'

def refresh_yahoo_token(oauth_token, oauth_secret, oauth_session_handle):
    """make call to refresh access token
   """
    
    base_url = 'https://api.login.yahoo.com/oauth/v2/get_token?'
    params = {
            'oauth_consumer_key': consumer_key,
            'oauth_signature_method' :'plaintext',
            'oauth_version': '1.0',
            'oauth_token' : oauth_token,
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time()),
            'oauth_session_handle': oauth_session_handle
            }

    pass


def get_yahoo_api_data(url, oauth_token, oauth_token_secret, extras=None):
    
    base_url = 'http://fantasysports.yahooapis.com/fantasy/v2/'
    params = {
            'format': 'json',
            'oauth_version': "1.0",
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time()),
            }
    if extras:
        params = dict(params.items() + extras.items())
    
    token = oauth.Token(key=oauth_token, secret=oauth_token_secret)
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    
    params['oauth_token'] = token.key
    params['oauth_consumer_key'] = consumer.key
    
    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    
    oauth_request = oauth.Request.from_consumer_and_token(consumer, token=token, http_method='GET', http_url=base_url+url, parameters=params)
    oauth_request.sign_request(signature_method, consumer, token)
    
    url = oauth_request.to_url()
    resp, content = httplib2.Http.request(oauth.Client(consumer), url, 'GET')
    
    #return resp, content
    return resp, json.loads(content)






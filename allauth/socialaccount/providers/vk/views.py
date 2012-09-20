import urllib
import random
import time
from md5 import md5

from django.contrib.auth.models import User

from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)

from allauth.socialaccount import requests
from allauth.socialaccount.models import SocialLogin, SocialAccount

from provider import VKProvider

class VKOAuth2Adapter(OAuth2Adapter):
    provider_id = VKProvider.id
    access_token_url = 'https://oauth.vk.com/access_token'
    authorize_url = 'http://oauth.vk.com/authorize'
    profile_url = 'http://api.vk.com/api.php'

    def complete_login(self, request, app, token):
        params = {
            'api_id': str(app.key),
            'format': 'json',
            'sid': token.token,
            'method': 'getProfiles',
            'uids': '2630606',
            'v': '2.0',
            'timestamp': str(time.time()),
            'random': str(int(random.random()*10000000)),
        }
        p = ''.join((
            ''.join((k+'='+params[k] for k in sorted(params))),
            app.secret
        ))
        params['sig'] = md5(p).hexdigest()
        resp = requests.get(self.profile_url, params)
        extra_data = resp.json['response'][0]
        uid = str(extra_data['uid'])
        user = User(last_name=extra_data.get('last_name', ''),
                    first_name=extra_data.get('first_name', ''))
        account = SocialAccount(extra_data=extra_data,
                                uid=uid,
                                provider=self.provider_id,
                                user=user)
        return SocialLogin(account)

oauth2_login = OAuth2LoginView.adapter_view(VKOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(VKOAuth2Adapter)



from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class VKAccount(ProviderAccount):
    def get_profile_url(self):
        return self.account.extra_data.get('link')

    def get_avatar_url(self):
        return self.account.extra_data.get('picture')

    def __unicode__(self):
        dflt = super(VKAccount, self).__unicode__()
        return ' '.join((
            self.account.extra_data.get('first_name', ''), 
            self.account.extra_data.get('last_name', '')
        )) or dflt


class VKProvider(OAuth2Provider):
    id = 'vk'
    name = 'VK.com'
    package = 'allauth.socialaccount.providers.vk'
    account_class = VKAccount

providers.registry.register(VKProvider)

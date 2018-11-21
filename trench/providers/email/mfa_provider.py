from trench.providers.base import BaseMFAProvider


class EmailProvider(BaseMFAProvider):
    id = 'email'
    name = 'E-mail'


mfa_providers = [EmailProvider]

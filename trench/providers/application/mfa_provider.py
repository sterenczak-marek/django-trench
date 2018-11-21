from trench.providers.base import BaseMFAProvider


class ApplicationProvider(BaseMFAProvider):
    id = 'app'
    name = 'Application'


mfa_providers = [ApplicationProvider]

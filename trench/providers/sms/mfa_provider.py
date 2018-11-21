from trench.providers.base import BaseMFAProvider
from .handlers import SmsAPIBackend


class SmsMFAProvider(BaseMFAProvider):
    id = 'sms'
    name = 'SMS'


mfa_providers = [SmsMFAProvider]

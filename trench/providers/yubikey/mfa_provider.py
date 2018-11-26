
from yubico_client.yubico import Yubico
from yubico_client.yubico_exceptions import YubicoError

from trench.providers.base import BaseMFAProvider

from . import MFA_YUBIKEY_ID


class YubiKeyMFAProvider(BaseMFAProvider):
    id = MFA_YUBIKEY_ID
    name = 'YubiKey'

    _mfa_model_class = 'yubikey.YubiKeyMFAMethod'
    _mfa_model_serializer = 'trench.providers.yubikey.serializers.YubiKeyFMAMethodSerializer'

    USE_MODEL_SERIALIZER_TO_ACTIVATION = True

    def validate_otp_code(self, code, mfa_obj):

        real_instance = self.get_real_instance(mfa_obj)

        return (
            len(code) == 44 and
            real_instance.yubikey_id == code[:12] and
            self._verify_yubikey_otp(code)
        )

    def _verify_yubikey_otp(self, code):
        client = Yubico(self.conf['YUBICLOUD_CLIENT_ID'])

        try:
            return client.verify(code, timestamp=True)

        except (YubicoError, Exception):
            return False


mfa_providers = [YubiKeyMFAProvider]

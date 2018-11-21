from trench.settings import api_settings

from yubico_client.yubico import Yubico
from yubico_client.yubico_exceptions import YubicoError


def validate_yubikey(code, user_public_id):
    conf = api_settings.MFA_METHODS['yubi']

    if code[:12] == user_public_id:

        client = Yubico(conf.get('YUBICLOUD_CLIENT_ID', 16))

        try:
            return client.verify(code)

        except YubicoError:

            return False

    return False

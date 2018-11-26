from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from trench.models import MFAMethod


class YubiKeyMFAMethod(MFAMethod):
    """
    Base model with MFA information linked to user.
    """

    yubikey_id = models.CharField(
        _('yubikey_id'),
        validators=[MinLengthValidator(12)],
        max_length=12
    )

    class Meta:
        verbose_name = _('YubiKey MFA Method')
        verbose_name_plural = _('YubiKey MFA Methods')

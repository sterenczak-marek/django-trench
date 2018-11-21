from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from trench import providers


class MFAMethod(models.Model):
    """
    Base model with MFA information linked to user.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='mfa_methods',
    )
    name = models.CharField(
        _('name'),
        max_length=255,
        choices=providers.registry.as_choices()
    )
    secret = models.CharField(
        _('secret'),
        max_length=20,
    )
    is_primary = models.BooleanField(
        _('is primary'),
        default=False,
    )
    is_active = models.BooleanField(
        _('is active'),
        default=False,
    )
    backup_codes = models.CharField(
        _('backup codes'),
        max_length=255,
        blank=True,
    )

    class Meta:
        verbose_name = _('MFA Method')
        verbose_name_plural = _('MFA Methods')

    def __str__(self):
        return '{} (User: {})'.format(self.name, self.user)

    def remove_backup_code(self, code):
        codes = self.backup_codes.split(',')
        if code in codes:
            codes.remove(code)
            self.backup_codes = ','.join(codes)
            self.save()

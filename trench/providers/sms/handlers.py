from smsapi.client import SmsApiPlClient

from django.utils.translation import gettext_lazy as _

from trench.providers.base import AbstractMessageDispatcher
from twilio.rest import Client


class AbstractSMSBackend(AbstractMessageDispatcher):

    SMS_BODY = _('Your verification code is: ')

    def dispatch_message(self):
        """
        Sends a SMS with verification code.
        """

        code = self.create_code()
        self.send_sms(self.to, code)

        return {
            'message': _('SMS message with MFA code had been sent.')
        }  # pragma: no cover # noqa

    def send_sms(self, user_mobile, code):
        raise NotImplementedError("Class %s must implement `send_sms` method" % self.__class__.__name__)


class SmsAPIBackend(AbstractSMSBackend):

    def send_sms(self, user_mobile, code):
        client = self.provider_auth()

        kwargs = {}
        if self.conf.get('SMSAPI_FROM_NUMBER'):
            kwargs['from_'] = self.conf.get('SMSAPI_FROM_NUMBER')  # pragma: no cover

        client.sms.send(
            message=self.SMS_BODY + code,
            to=user_mobile,
            **kwargs
        )

    def provider_auth(self):
        return SmsApiPlClient(
            access_token=self.conf['SMSAPI_ACCESS_TOKEN']
        )


class TwilioBackend(AbstractSMSBackend):

    def send_sms(self, user_mobile, code):
        client = self.provider_auth()
        client.messages.create(
            body=self.SMS_BODY + code,
            to=user_mobile,
            from_=self.conf.get('TWILIO_VERIFIED_FROM_NUMBER')
        )

    def provider_auth(self):
        return Client(
            self.conf.get('TWILIO_ACCOUNT_SID'),
            self.conf.get('TWILIO_AUTH_TOKEN'),
        )

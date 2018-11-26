from django.apps import apps
from django.utils.functional import cached_property
from rest_framework.settings import perform_import

from trench.exceptions import MissingSourceFieldAttribute
from trench.settings import api_settings
from trench.utils import (
    validate_code,
    get_nested_attr_value,
    create_otp_code,
)


class AbstractMessageDispatcher:
    def __init__(self, user, obj, conf):
        self.user = user
        self.obj = obj
        self.conf = conf
        self.to = ''

        if 'SOURCE_FIELD' in conf:
            value = get_nested_attr_value(user, conf['SOURCE_FIELD'])
            if not value:
                raise MissingSourceFieldAttribute(  # pragma: no cover
                    'Could not retrieve attribute '
                    '{} for given user'.format(conf['SOURCE_FIELD'])
                )
            self.to = value

    def dispatch_message(self):
        pass  # pragma: no cover

    def create_code(self):
        return create_otp_code(self.obj.secret)


class BaseMFAProvider(object):

    slug = None

    id = None
    name = None

    _mfa_model_class = 'trench.MFAMethod'
    _mfa_model_serializer = 'trench.serializers.UserMFAMethodSerializer'

    USE_MODEL_SERIALIZER_TO_ACTIVATION = False

    @cached_property
    def conf(self):
        return api_settings.MFA_METHODS.get(self.id, {})

    @cached_property
    def MFAModel(self):
        return apps.get_model(self._mfa_model_class)

    @cached_property
    def model_serializer(self):
        return perform_import(
            self._mfa_model_serializer,
            'MODEL_SERIALIZER'
        )

    def get_handler(self, user, mfa_method):
        return self.conf['HANDLER'](
            user,
            mfa_method,
            self.conf
        )

    def get_real_instance(self, instance):
        return self.MFAModel.objects.get(pk=instance.pk)

    def validate_otp_code(self, code, mfa_obj):
        validity_period = self.conf.get('validity_period', api_settings.DEFAULT_VALIDITY_PERIOD)

        return len(code) == 6 and validate_code(code, mfa_obj.secret, validity_period)

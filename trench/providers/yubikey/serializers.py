from rest_framework import serializers

from .models import YubiKeyMFAMethod


class YubiKeyFMAMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = YubiKeyMFAMethod
        fields = ('name', 'is_primary', 'yubikey_id', )
        read_only_fields = ('name', 'is_primary', )

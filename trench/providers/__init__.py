import importlib

from collections import OrderedDict

from django.conf import settings
from django.http import Http404


class MFAMethodRegistry(object):
    """
    Class generated the same way as django-allauth registry
    """

    def __init__(self):
        self.provider_map = OrderedDict()
        self.loaded = False

    def register(self, cls):
        self.provider_map[cls.id] = cls

    def by_id(self, _id):
        self.load()
        return self.provider_map[_id]()

    def get_or_404(self, _id):
        try:
            return self.by_id(_id)

        except KeyError:
            raise Http404

    def as_choices(self):
        self.load()
        for provider_cls in self.provider_map.values():
            yield (provider_cls.id, provider_cls.name)

    def load(self):
        if not self.loaded:

            for app in settings.INSTALLED_APPS:

                try:
                    provider_module = importlib.import_module(
                        app + '.mfa_provider'
                    )
                except ModuleNotFoundError:
                    pass
                else:
                    for cls in getattr(
                        provider_module, 'mfa_providers', []
                    ):
                        self.register(cls)
            self.loaded = True


registry = MFAMethodRegistry()

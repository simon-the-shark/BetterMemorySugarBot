import os

from django.core.files.storage import FileSystemStorage
from django.conf import settings


class OverwriteStorage(FileSystemStorage):
    '''
    File system storage which overwrite files if names are duplicated
    '''

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.STATIC_ROOT, "uplouded", name))
        return super().get_available_name(name, max_length)

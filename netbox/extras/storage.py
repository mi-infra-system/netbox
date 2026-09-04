from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.functional import cached_property


class ScriptFileSystemStorage(FileSystemStorage):
    """
    Custom local storage for scripts. The default file storage is rooted at
    MEDIA_ROOT, while scripts and reports may live outside that directory.
    """
    @cached_property
    def base_location(self):
        return settings.SCRIPTS_ROOT

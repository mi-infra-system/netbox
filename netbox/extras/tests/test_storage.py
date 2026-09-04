import tempfile

from django.core.files.base import ContentFile
from django.test import SimpleTestCase, override_settings

from extras.storage import ScriptFileSystemStorage


class ScriptFileSystemStorageTestCase(SimpleTestCase):

    def test_local_script_file_round_trip(self):
        with tempfile.TemporaryDirectory() as scripts_root:
            with override_settings(SCRIPTS_ROOT=scripts_root):
                storage = ScriptFileSystemStorage(allow_overwrite=True)
                name = storage.save('storage-regression.py', ContentFile(b'answer = 42'))

                self.assertEqual(name, 'storage-regression.py')
                with storage.open(name, 'rb') as script_file:
                    self.assertEqual(script_file.read(), b'answer = 42')

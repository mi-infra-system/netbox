import unittest

from users.utils import clean_username


class CleanUsernameTestCase(unittest.TestCase):
    """Keep local username cleaning equivalent to the former upstream helper."""

    def test_upstream_equivalent_cleaning(self):
        cases = {
            'plain-user': 'plain-user',
            'user@example.com': 'user@example.com',
            'user+tag_name': 'user+tag_name',
            'user:name': 'username',
            'user/name?': 'username',
            'ümlaut-user': 'mlaut-user',
            'user\u200bname': 'username',
        }

        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(clean_username(value), expected)

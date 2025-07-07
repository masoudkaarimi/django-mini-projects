from django.test import TestCase


class AccountTestCase(TestCase):
    fixtures = ("users", "profiles")

    def setUp(self):
        pass

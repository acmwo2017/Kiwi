import unittest

from django.conf import settings
from django.core.cache import cache

from tcms.rpc.tests.utils import APITestCase

if 'tcms.bugs.apps.AppConfig' not in settings.INSTALLED_APPS:
    raise unittest.SkipTest('tcms.bugs is disabled')


class TestBug(APITestCase):

    def test_get_details_from_cache(self):
        url = "http://some.url"
        expected_result = {
            'title': 'Bug from cache',
            'description': 'This bug came from the Django cache'
        }
        cache.set(url, expected_result)
        result = self.rpc_client.Bug.details(url)

        self.assertEqual(result, expected_result)

    def test_empty_details_when_tracker_does_not_exist(self):
        url = "http://unknown-tracker.url"

        result = self.rpc_client.Bug.details(url)
        self.assertEqual(result, {})

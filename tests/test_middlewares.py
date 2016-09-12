from datetime import datetime
from testfixtures import LogCapture

from django.forms.models import model_to_dict
from django.test import TestCase
from django.conf import settings

from library.models import RequestLog
import pytest


@pytest.mark.usefixtures('superuser')
class RequestLogMiddlewareTestCase(TestCase):
    def tearDown(self):
        RequestLog.objects.all().delete()

    def test_request_login_middleware(self):
        """Should create an instance of RequestLog for each request attended"""
        # Preconditions
        self.assertEqual(RequestLog.objects.count(), 0)
        self.client.login(username=self.user.username, password='abc123')
        params = {'foo': 'bar'}
        self.client.get('/admin/', params, follow=True)

        # Postconditions
        self.assertEqual(RequestLog.objects.count(), 1)
        log = RequestLog.objects.first()
        self.assertEqual(log.method, 'GET')
        self.assertEqual(log.code, 200)
        self.assertEqual(log.url, '/admin/')
        self.assertEqual(log.full_url, '/admin/?foo=bar')
        self.assertEqual(log.ip, '127.0.0.1')
        self.assertEqual(log.get_params, {'foo': 'bar'})
        self.assertEqual(log.user_agent, None)
        self.assertEqual(log.query_count, 0)
        self.assertTrue(isinstance(log.timestamp, datetime))
        self.assertTrue(isinstance(log.duration_in_seconds, int))

    def test_failed_login(self):
        assert RequestLog.objects.count() == 0
        self.client.login(username='nobody', password='invalid')
        self.client.get('/admin/', {'foo': 'bar'}, follow=False)

        assert RequestLog.objects.count() == 1
        log = RequestLog.objects.first()
        assert log.code == 302
        assert log.method == 'GET'

        # print(model_to_dict(RequestLog.objects.first()))
        # assert 0

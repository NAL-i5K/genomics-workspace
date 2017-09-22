from django.test import SimpleTestCase
import celery

class CeleryTestCase(SimpleTestCase):
    def test_celery_run(self):
        d = celery.app.control.inspect().stats()
        self.assertIsNotNone(d)
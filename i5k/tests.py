from django.test import SimpleTestCase
import celery
import subprocess

class CeleryTestCase(SimpleTestCase):
    def test_rabbitmq_run(self):
        # example output of `rabbitmq status` command can be found at https://www.rabbitmq.com/troubleshooting.html
        try:
            p = subprocess.check_output(['rabbitmqctl', 'status'], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            p = e.output
        is_error = 'Error: unable' in p.split('\n')[1]
        self.assertEqual(is_error, False)

    def test_celery_run(self):
        d = celery.app.control.inspect().stats()
        self.assertIsNotNone(d)
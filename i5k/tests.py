from django.test import SimpleTestCase
import celery
from celery import Celery
import subprocess
import multiprocessing

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

    def test_celery_beat_run(self):
        pass

    def test_celery_worker_process(self):
        app = Celery('i5k')
        keys = celery.app.control.inspect(app=app).stats().keys()
        num_node = len(keys)
        self.assertEqual(num_node, 1)
        num_cpu = multiprocessing.cpu_count()
        num_prpocess = len(celery.app.control.inspect().stats()[keys[0]]['pool']['processes'])
        self.assertEqual(num_prpocess, num_cpu)

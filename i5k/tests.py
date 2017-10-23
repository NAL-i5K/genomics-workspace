from django.test import SimpleTestCase
import celery
from celery import Celery
import subprocess
from threading import Timer

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
        kill = lambda process: process.kill()
        my_command = subprocess.Popen(['celery', '-A', 'i5k', 'beat'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        my_timer = Timer(5, kill, [my_command])
        try:
            my_timer.start()
            stdout, stderr = my_command.communicate()
        finally:
            my_timer.cancel()
        self.assertEqual("Seems we're already running?" in stderr, True)
        self.assertNotEqual(stdout, '')

    def test_celery_worker_process(self):
        app = Celery('i5k')
        queues = celery.app.control.inspect(app=app).active_queues()
        is_run = False
        for inst in queues:
            for j, queue in enumerate(queues[inst]):
                if queue['name'] == 'i5k':
                    is_run = True
                    instance = inst
                    break
        self.assertEqual(is_run, True)
        num_prpocess = len(celery.app.control.inspect(app=app).stats()[instance]['pool']['processes'])
        self.assertEqual(num_prpocess, 3)

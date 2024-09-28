from django.test import TransactionTestCase
from django.test.runner import DiscoverRunner

# Custom DiscoverRunner as stated in https://stackoverflow.com/a/26396157/5363040
class MyDiscoverRunner(DiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        """
        Run the unit tests for all the test labels in the provided list.

        Test labels should be dotted Python paths to test modules, test
        classes, or test methods.

        A list of 'extra' tests may also be provided; these tests
        will be added to the test suite.

        If any of the tests in the test suite inherit from
        ``django.test.TransactionTestCase``, databases will be setup.
        Otherwise, databases will not be set up.

        Returns the number of tests that failed.
        """
        self.setup_test_environment()
        suite = self.build_suite(test_labels, extra_tests)
        # ----------------- First Addition --------------
        need_databases = any(isinstance(test_case, TransactionTestCase)
                             for test_case in suite)
        old_config = None
        if need_databases:
        # --------------- End First Addition ------------
            old_config = self.setup_databases()
        result = self.run_suite(suite)
        # ----------------- Second Addition -------------
        if need_databases:
        # --------------- End Second Addition -----------
            self.teardown_databases(old_config)
        self.teardown_test_environment()
        return self.suite_result(suite, result)

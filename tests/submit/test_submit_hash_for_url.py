# content of test_pyconv.py

import os

from base_test import BaseTest

# we reuse a bit of pytest's own testing machinery, this should eventually come
# from a separatedly installable pytest-cli plugin.
pytest_plugins = ["pytester"]


class TestSubmitHashForUrl(BaseTest):

    expected_response = {'there': 'is'}

    def get_action_name(self):
        return 'submit_hash_for_url'

    def init_request_scenario(self):
        os.environ['TEST_SCENARIO'] = 'submit.submit_hash_for_url'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'google.com')
        self.see_response(self.expected_response)

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'google.com', '-v')
        self.see_headers()
        self.see_response(self.expected_response)
        self.see_sent_params('POST', {'url': 'google.com'})

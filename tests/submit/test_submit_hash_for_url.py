import os

from base_test import BaseTest


pytest_plugins = ["pytester"]


class TestSubmitHashForUrl(BaseTest):

    expected_response = {'there': 'is'}

    def get_action_name(self):
        return 'submit_hash_for_url'

    def init_request_scenario(self):
        os.environ['VX_TEST_SCENARIO'] = 'submit.submit_hash_for_url'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'example.com')
        self.see_response(self.expected_response)

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'example.com', '-v')
        self.see_headers()
        self.see_response(self.expected_response)
        self.see_sent_params('POST', {'url': 'example.com'})

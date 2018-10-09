import os

from base_test import BaseTest


pytest_plugins = ["pytester"]


class TestScanUrlToFile(BaseTest):

    expected_response = {'there': 'is'}

    def get_action_name(self):
        return 'scan_url_to_file'

    def init_request_scenario(self):
        os.environ['TEST_SCENARIO'] = 'scan.scan_url_to_file'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'google.com', 'all')
        self.see_response(self.expected_response)

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'google.com', 'all', '-v')
        self.see_headers()
        self.see_response(self.expected_response)
        self.see_sent_params('POST', {'url': 'google.com', 'scan_type': 'all'})

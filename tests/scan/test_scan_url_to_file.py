import os

from base_test import BaseTest


pytest_plugins = ["pytester"]


class TestScanUrlToFile(BaseTest):

    expected_response = {'there': 'is'}

    def get_action_name(self):
        return 'scan_url_to_file'

    def init_request_scenario(self):
        os.environ['VX_TEST_SCENARIO'] = 'scan.scan_url_to_file'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'example.com', 'all')
        self.see_response(self.expected_response)

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'example.com', 'all', '-v')
        self.see_headers()
        self.see_response(self.expected_response)
        self.see_sent_params('POST', {'url': 'example.com', 'scan_type': 'all', 'no_share_third_party': 1, 'allow_community_access': 1})

import os

from base_test import BaseTest


pytest_plugins = ["pytester"]


class TestScanScan(BaseTest):

    expected_response = {'there': 'is'}

    def get_action_name(self):
        return 'scan_get_result'

    def init_request_scenario(self):
        os.environ['VX_TEST_SCENARIO'] = 'scan.scan_scan'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test')
        self.see_response(self.expected_response)

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test', '-v')
        self.see_headers()
        self.see_response(self.expected_response)
        self.see_sent_params('GET', {})

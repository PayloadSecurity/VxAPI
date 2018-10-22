import os

from base_test import BaseTest


pytest_plugins = ["pytester"]


class TestScanScan(BaseTest):

    def get_action_name(self):
        return 'scan_get_scanners'

    def init_request_scenario(self):
        os.environ['VX_TEST_SCENARIO'] = 'scan.scan_state'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name())
        self.see_response([{"available": True, 'name': 'parrot'}])

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), '-v')
        self.see_headers()
        self.see_response([{"available": False, 'name': 'cat'}, {"available": True, 'name': 'parrot'}, {"available": False, 'name': 'qwerty'}])
        self.see_sent_params('GET', {})

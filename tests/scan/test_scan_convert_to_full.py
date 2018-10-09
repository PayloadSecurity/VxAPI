# content of test_pyconv.py

import os

from base_test import BaseTest

# we reuse a bit of pytest's own testing machinery, this should eventually come
# from a separatedly installable pytest-cli plugin.
pytest_plugins = ["pytester"]


class TestScanConvertToFull(BaseTest):

    expected_response = {'there': 'is'}

    def get_action_name(self):
        return 'scan_convert_to_full'

    def init_request_scenario(self):
        os.environ['TEST_SCENARIO'] = 'scan.scan_convert_to_full'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test', '5')
        self.see_response(self.expected_response)

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test', '5', '-v')
        self.see_headers()
        self.see_response(self.expected_response)
        self.see_sent_params('POST', {'environment_id': 5})

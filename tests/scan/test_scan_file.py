# content of test_pyconv.py

import os

from base_test import BaseTest

# we reuse a bit of pytest's own testing machinery, this should eventually come
# from a separatedly installable pytest-cli plugin.
pytest_plugins = ["pytester"]


class TestScanFile(BaseTest):

    expected_response = {'there': 'is'}

    def get_action_name(self):
        return 'scan_file'

    def init_request_scenario(self):
        os.environ['TEST_SCENARIO'] = 'scan.scan_file'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'tests/_data/hashes', 'all')
        self.see_response(self.expected_response)

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'tests/_data/hashes', 'all', '-v')
        self.see_headers()
        self.see_response(self.expected_response)
        self.see_sent_files('tests/_data/hashes')
        self.see_sent_params('POST', {'scan_type': 'all'})

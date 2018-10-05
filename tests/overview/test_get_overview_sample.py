# content of test_pyconv.py

import subprocess
import os

from base_test import BaseTest

# we reuse a bit of pytest's own testing machinery, this should eventually come
# from a separatedly installable pytest-cli plugin.
pytest_plugins = ["pytester"]


class TestGetOverviewSample(BaseTest):

    expected_response = b'Lorem ipsum dolor sit amet.\n'

    def get_action_name(self):
        return 'overview_download_sample'

    def init_request_scenario(self):
        os.environ['TEST_SCENARIO'] = 'overview.get_overview_sample'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test')
        print(self.output)
        self.see_file_response('output/overview_download_sample-test-my-archive.bin', self.expected_response, mode='rb')

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test', '-v')
        self.see_headers()
        self.see_file_response('output/overview_download_sample-test-my-archive.bin', self.expected_response, mode='rb')

import subprocess
import os

from base_test import BaseTest


pytest_plugins = ["pytester"]


class TestGetOverviewSample(BaseTest):

    expected_hash = '98bdbd3fb298c89cc8ad98fa42c6ea1b819701cd3e5869bc09d1498d333d587c'

    def get_action_name(self):
        return 'overview_download_sample'

    def init_request_scenario(self):
        os.environ['VX_TEST_SCENARIO'] = 'overview.overview_sample'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test')
        self.see_file_response('output/overview_download_sample-test-my-archive.bin', self.expected_hash)

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test', '-v')
        self.see_headers()
        self.see_file_response('output/overview_download_sample-test-my-archive.bin', self.expected_hash)

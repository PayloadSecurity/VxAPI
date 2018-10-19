import subprocess
import os

from base_test import BaseTest


pytest_plugins = ["pytester"]


class TestGetOverview(BaseTest):

    expected_response = {'pies': 'to'}

    def get_action_name(self):
        return 'overview_get'

    def init_request_scenario(self):
        os.environ['VX_TEST_SCENARIO'] = 'overview.overview'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test')
        self.see_response(self.expected_response)

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test', '-v')
        self.see_headers()
        self.see_response(self.expected_response)

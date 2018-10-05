# content of test_pyconv.py

import subprocess
import os

from base_test import BaseTest

# we reuse a bit of pytest's own testing machinery, this should eventually come
# from a separatedly installable pytest-cli plugin.
pytest_plugins = ["pytester"]


class TestGetOverviewSummary(BaseTest):

    expected_response = {'pies': 'to'}

    def get_action_name(self):
        return 'overview_get_summary'

    def init_request_scenario(self):
        os.environ['TEST_SCENARIO'] = 'overview.get_overview_summary'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test')
        self.see_response(self.expected_response)

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test', '-v')
        self.see_headers()
        self.see_response(self.expected_response)

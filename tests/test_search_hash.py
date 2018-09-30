# content of test_pyconv.py

import pytest
import subprocess
import os

from base_test import BaseTest

# we reuse a bit of pytest's own testing machinery, this should eventually come
# from a separatedly installable pytest-cli plugin.
pytest_plugins = ["pytester"]


class TestSearchHash(BaseTest):

    expected_response = {'pies': 'to'}

    def get_action_name(self):
        return 'search_hash'

    def init_request_scenario(self):
        os.environ['TEST_SCENARIO'] = 'search_hash'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        code, output = run_command(self.get_action_name(), 'test')
        self.see_response(self.expected_response, output)

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        code, output = run_command(self.get_action_name(), 'test', '-v')
        self.see_headers(output)
        self.see_response(self.expected_response, output)

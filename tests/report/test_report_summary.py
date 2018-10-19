import pytest
import subprocess
import os

from base_test import BaseTest


pytest_plugins = ["pytester"]


class TestReportSummary(BaseTest):

    expected_response = [{'doc': 'first'}, {'doc': 'second'}]

    def get_action_name(self):
        return 'report_get_summary'

    def init_request_scenario(self):
        os.environ['VX_TEST_SCENARIO'] = 'report.report_summary'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test')
        self.see_response(self.expected_response)

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test', '-v')
        self.see_sent_params('GET', {})
        self.see_headers()
        self.see_response(self.expected_response)

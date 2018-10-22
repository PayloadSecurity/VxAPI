import pytest
import subprocess
import os

from base_test import BaseTest


pytest_plugins = ["pytester"]


class TestReportBulkSummary(BaseTest):

    expected_response = [{'doc': 'first'}, {'doc': 'second'}]

    def get_action_name(self):
        return 'report_get_bulk_summary'

    def init_request_scenario(self):
        os.environ['VX_TEST_SCENARIO'] = 'report.report_bulk_summary'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'tests/_data/hashes')
        self.see_response(self.expected_response)

    def test_base_query_with_not_existing_file(self, run_command):
        self.init_request_scenario()
        run_command(self.get_action_name(), 'not_existing_file')
        self.see_missing_file_command_state()

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'tests/_data/hashes', '-v')
        self.see_sent_params('POST', {'hashes[0]': 'qwerty', 'hashes[1]': 'some_other', 'hashes[2]': 'hash'})
        self.see_headers()
        self.see_response(self.expected_response)

    def test_verbose_query_with_not_existing_file(self, run_command):
        self.init_request_scenario()
        run_command(self.get_action_name(), 'not_existing_file', '-v')
        self.see_missing_file_command_state()

import pytest
import os

from base_test import BaseTest


pytest_plugins = ["pytester"]


class TestSearchStates(BaseTest):

    expected_response = [{'doc': 'first'}, {'doc': 'second'}]

    def get_action_name(self):
        return 'search_states'

    def init_request_scenario(self):
        os.environ['VX_TEST_SCENARIO'] = 'search.search_states'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'tests/_data/ids')
        self.see_response(self.expected_response)

    def test_base_query_with_not_existing_file(self, run_command):
        self.init_request_scenario()
        run_command(self.get_action_name(), 'not_existing_file')
        self.see_missing_file_command_state()

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'tests/_data/ids', '-v')
        self.see_sent_params('POST', {'ids[0]': 'qwerty:1', 'ids[1]': 'some_other', 'ids[2]': 'hash'})
        self.see_headers()
        self.see_response(self.expected_response)

    def test_verbose_query_with_not_existing_file(self, run_command):
        self.init_request_scenario()
        run_command(self.get_action_name(), 'not_existing_file', '-v')
        self.see_missing_file_command_state()

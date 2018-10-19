import pytest
import subprocess
import os

from base_test import BaseTest


pytest_plugins = ["pytester"]


class TestSearchTerms(BaseTest):

    expected_response = [{"doc": "first"}, {"doc": "second"}]

    def get_action_name(self):
        return 'search_terms'

    def init_request_scenario(self):
        os.environ['VX_TEST_SCENARIO'] = 'search.search_terms'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), '--filename', 'exe')
        self.see_response(self.expected_response)

    @pytest.mark.parametrize("command_args,expected_sent_params", [
        (['--filename', 'exe'], {'filename': 'exe'}),
        (['--av-detect', '70-80', '--filename', 'exe', '--similar-to', 'qwerty'], {'filename': 'exe', 'av_detect': '70-80', 'similar_to': 'qwerty'}),
        (['--av-detect', '70', '--filename', 'exe', '--similar-to', 'qwerty'], {'filename': 'exe', 'av_detect': '70', 'similar_to': 'qwerty'}),
    ])
    def test_verbose_query(self, run_command, command_args, expected_sent_params):
        self.init_request_scenario()

        final_command_args = [self.get_action_name(), '-v'] + command_args
        run_command(*final_command_args)
        self.see_sent_params('POST', expected_sent_params)
        self.see_headers()
        self.see_response(self.expected_response)

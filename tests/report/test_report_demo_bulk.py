import pytest
import subprocess
import os

from base_test import BaseTest


pytest_plugins = ["pytester"]


class TestReportDemoBulk(BaseTest):

    expected_hash = '8b585baa0b8f4bea3af85f93eda4c164d3c577b34856e6ca9d923a676e95a8e9'

    def get_action_name(self):
        return 'report_get_demo_bulk'

    def init_request_scenario(self):
        os.environ['VX_TEST_SCENARIO'] = 'report.report_demo_bulk'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name())
        self.see_file_response('output/report_get_demo_bulk-archive-file.zip', self.expected_hash)

    @pytest.mark.parametrize("command_args,expected_sent_params", [
        ([], {'modify_hash': False, 'av_min': 5, 'av_max': 15, 'look_back_size': 400}),
        (['--modify-hash', '--av-min', '0', '--av-max', '50', '--look-back-size', '500'], {'modify_hash': True, 'av_min': 0, 'av_max': 50, 'look_back_size': 500}),
    ])
    def test_verbose_query(self, run_command, command_args, expected_sent_params):
        self.init_request_scenario()

        final_command_args = [self.get_action_name(), '-v'] + command_args
        run_command(*final_command_args)
        self.see_sent_params('GET', expected_sent_params)
        self.see_headers()
        self.see_file_response('output/report_get_demo_bulk-archive-file.zip', self.expected_hash)

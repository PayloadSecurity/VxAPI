
import subprocess
import os

from base_test import BaseTest


pytest_plugins = ['pytester']


class TestFeed(BaseTest):

    expected_response = {'pies': 'to'}

    def get_action_name(self):
        return 'feed_get_latest'

    def init_request_scenario(self):
        os.environ['VX_TEST_SCENARIO'] = 'feed.feed_latest'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name())
        self.see_response(self.expected_response)

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), '-v')
        self.see_headers()
        self.see_sent_params('GET', {})
        self.see_response(self.expected_response)

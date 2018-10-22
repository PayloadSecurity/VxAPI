import os

from base_test import BaseTest

pytest_plugins = ["pytester"]


class TestKeyCreate(BaseTest):

    expected_response = {'pies': 'to'}

    def get_action_name(self):
        return 'key_create'

    def init_request_scenario(self):
        os.environ['VX_TEST_SCENARIO'] = 'key.key_create'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test')
        self.see_response(self.expected_response)

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test', '-v')
        self.see_headers()
        self.see_sent_params('POST', {'uid': 'test'})
        self.see_response(self.expected_response)

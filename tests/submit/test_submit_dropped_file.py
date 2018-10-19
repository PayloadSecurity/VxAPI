import os

from base_test import BaseTest


pytest_plugins = ["pytester"]


class TestSubmitDroppedFile(BaseTest):

    expected_response = {'there': 'is'}

    def get_action_name(self):
        return 'submit_dropped_file'

    def init_request_scenario(self):
        os.environ['VX_TEST_SCENARIO'] = 'submit.submit_dropped_file'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'sha256:envId', 'sha256')
        self.see_response(self.expected_response)

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'sha256:envId', 'sha256', '-v')
        self.see_headers()
        self.see_response(self.expected_response)

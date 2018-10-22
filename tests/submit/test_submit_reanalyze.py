import os

from base_test import BaseTest


pytest_plugins = ["pytester"]


class TestSubmitReanalyze(BaseTest):

    expected_response = {'there': 'is'}

    def get_action_name(self):
        return 'submit_reanalyze'

    def init_request_scenario(self):
        os.environ['VX_TEST_SCENARIO'] = 'submit.submit_reanalyze'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'some_tmp_id')
        self.see_response(self.expected_response)

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'some_tmp_id', '-v')
        self.see_headers()
        self.see_response(self.expected_response)
        self.see_sent_params('POST', {'id': 'some_tmp_id', 'no_share_third_party': 1})

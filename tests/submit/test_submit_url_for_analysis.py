import os

from base_test import BaseTest

pytest_plugins = ["pytester"]


class TestSubmitUrlForAnalysis(BaseTest):

    expected_response = {'there': 'is'}

    def get_action_name(self):
        return 'submit_url_for_analysis'

    def init_request_scenario(self):
        os.environ['VX_TEST_SCENARIO'] = 'submit.submit_url_for_analysis'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'example.com', '5')
        self.see_response(self.expected_response)

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'example.com', '5', '-v')
        self.see_headers()
        self.see_response(self.expected_response)
        self.see_sent_params('POST', {'url': 'example.com', 'environment_id': 5, 'no_share_third_party': 1, 'allow_community_access': 1})

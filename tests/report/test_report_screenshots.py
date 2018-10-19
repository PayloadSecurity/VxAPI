import os
import hashlib

from base_test import BaseTest


pytest_plugins = ["pytester"]


class TestReportScreenshots(BaseTest):

    expected_response = [
        {'name': 'image1.png', 'image': 'cXdlcnR5', 'date': 'd-m-y'},
        {'name': 'image2.png', 'image': 'dHl1aW9w', 'date': 'd-m-y'}
    ]

    def get_action_name(self):
        return 'report_get_screenshots'

    def init_request_scenario(self):
        os.environ['VX_TEST_SCENARIO'] = 'report.report_screenshots'

    def test_base_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test')
        self.see_response(self.expected_response)
        self.check_saved_screenshots()

    def test_verbose_query(self, run_command):
        self.init_request_scenario()

        run_command(self.get_action_name(), 'test', '-v')
        self.see_sent_params('GET', {})
        self.see_headers()
        self.see_response(self.expected_response)
        self.check_saved_screenshots()


    def check_saved_screenshots(self):
        output_path = 'output/{}-test'.format(self.get_action_name())
        input_path = 'tests/_data/screenshots'
        input_screenshots = sorted(os.listdir(input_path))
        output_screenshots = sorted(os.listdir(output_path))
        assert os.path.exists(output_path)
        assert input_screenshots == output_screenshots
        for name in input_screenshots:
            first_handler = open('{}/{}'.format(input_path, name), 'rb')
            second_handler = open('{}/{}'.format(output_path, name), 'rb')

            assert hashlib.sha256(first_handler.read()).hexdigest() == hashlib.sha256(second_handler.read()).hexdigest()



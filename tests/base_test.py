import json
import abc
import subprocess
import pytest

class BaseTest(object):

    output = None
    code = None

    @abc.abstractmethod
    def get_action_name(self):
        return

    @pytest.fixture
    def run_command(self):
        def do_run(*args):
            args = ['python3', 'vxapi.py'] + list(args)
            p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            (output, _) = p.communicate()
            output = output.decode('utf-8')
            self.output = output
            self.code = p.returncode

            return [p.returncode, output]

        return do_run

    def see_headers(self):
        assert 'Running \'VxWebService Python API Connector\'' in self.output
        assert 'API Limits for used API Key' in self.output
        assert 'Request was sent at' in self.output
        assert 'Received response at' in self.output
        assert 'Showing response' in self.output

    def see_successful_response_messages(self):
        assert 'Response status code: 200' in self.output
        assert 'Message: Your request was successfully processed by Falcon Sandbox' in self.output

    def see_response(self, dict):
        assert json.dumps(dict, indent=4, sort_keys=True, ensure_ascii=False) in self.output

    def see_sent_params(self, method, params):
        assert 'Sent {} params: {}'.format(method, params) in self.output

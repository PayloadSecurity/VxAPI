import json
import abc
import subprocess
import pytest
import os
import hashlib
import shutil


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
            print(output)

            return [p.returncode, output]

        return do_run

    def see_headers(self):
        assert 'Running \'VxWebService Python API Connector\'' in self.output
        assert 'API query limits for used API Key' in self.output
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

    def see_sent_files(self, filename):
        assert 'Sent files: {\'file\': <_io.BufferedReader name=\'' + filename + '\'>}' in self.output

    def see_reached_url(self, url_part):
        assert 'Endpoint URL: mock://my-webservice-instance/api/v2/{}'.format(url_part) in self.output

    def see_missing_file_command_state(self):
        assert self.code != 0
        assert 'No such file or directory:' in self.output

    def see_file_response(self, path, expected_file_hash, mode='rb'):
        prepared_file_path = os.path.dirname(os.path.realpath(__file__)).split('/')[:-1] + [path]
        final_output_path = '/'.join(prepared_file_path)

        assert 'Response contains files. They were saved in the output folder'.format(os.path.dirname(final_output_path)) in self.output

        file_handler = open(final_output_path, mode)

        assert hashlib.sha256(file_handler.read()).hexdigest() == expected_file_hash

    def remove_dir_content(self, dir_path): # TODO - move that logic to separated class, which is outside the test env
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)


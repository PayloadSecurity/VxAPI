import json
import abc


class BaseTest(object):

    @abc.abstractmethod
    def get_action_name(self):
        return

    def see_headers(self, output):
        assert 'Running \'VxWebService Python API Connector\'' in output
        assert 'API Limits for used API Key' in output
        assert 'Request was sent at' in output
        assert 'Received response at' in output
        assert 'Showing response' in output

    def see_successful_response_messages(self, output):
        assert 'Response status code: 200' in output
        assert 'Message: Your request was successfully processed by Falcon Sandbox' in output

    def see_response(self, dict, output):
        assert json.dumps(dict, indent=4, sort_keys=True, ensure_ascii=False) in output

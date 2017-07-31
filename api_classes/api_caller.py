from exceptions import OptionNotDeclaredError
from exceptions import ResponseObjectNotExistError
from exceptions import UrlBuildError
from exceptions import JsonParseError
from requests.auth import HTTPBasicAuth
import json


class ApiCaller:

    CONST_REQUEST_METHOD_GET = 'get'
    CONST_REQUEST_METHOD_POST = 'post'

    CONST_EXPECTED_DATA_TYPE_JSON = 'json'
    CONST_EXPECTED_DATA_TYPE_FILE = 'file'

    CONST_API_AUTH_LEVEL_RESTRICTED = 1
    CONST_API_AUTH_LEVEL_DEFAULT = 100
    CONST_API_AUTH_LEVEL_ELEVATED = 500
    CONST_API_AUTH_LEVEL_SUPER = 1000

    api_key = ''
    api_secret = ''

    server = ''
    endpoint_url = ''
    endpoint_auth_level = CONST_API_AUTH_LEVEL_RESTRICTED
    data = {}
    params = {}
    files = {}
    request_method_name = ''

    api_result_msg = ''
    api_unexpected_error_msg = 'Unexpected error has occurred (HTTP code: {}). Please try again later or contact with the support'
    api_unexpected_error_404_msg = 'Unexpected error has occurred (HTTP code: {}). This error is mostly occurring when called webservice is outdated and so does not support current action. If you believe it is an error, please contact with the support'
    api_success_msg = 'Your request was successfully processed by VxStream Sandbox'
    api_expected_error_msg = 'API error has occurred. HTTP code: {}, API error code: {}, message: \'{}\''
    response_msg_success_nature = False

    api_response = None
    api_expected_data_type = CONST_EXPECTED_DATA_TYPE_JSON
    api_response_json = {}

    def __init__(self, api_key: str, api_secret: str, server: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.server = server
        self.check_class_options()

    def check_class_options(self):
        requested_fields = ['request_method_name', 'endpoint_url']
        for requested_field in requested_fields:
            if getattr(self, requested_field) == '':
                raise OptionNotDeclaredError('Value for \'{}\' should be declared in class \'{}\'.'.format(requested_field, self.__class__.__name__))

    def call(self, request_handler, headers={'User-agent': 'VxApi Connector'}):
        if ':' in self.endpoint_url:
            raise UrlBuildError('Can\'t call API endpoint with url \'{}\', when some placeholders are still not filled.'.format(self.endpoint_url))

        caller_function = getattr(request_handler, self.request_method_name)
        self.api_response = caller_function(self.server + self.endpoint_url, data=self.data, params=self.params, files=self.files, headers=headers, verify=False, auth=HTTPBasicAuth(self.api_key, self.api_secret))
        self.api_result_msg = self.prepare_response_msg()

    def attach_data(self, options):
        self.data = options
        self.build_url(self.data)

    def attach_params(self, params):
        self.params = params
        self.build_url(self.params)

    def attach_files(self, files):
        self.files = files

    def prepare_response_msg(self) -> str:
        if self.api_response is None:
            raise ResponseObjectNotExistError('It\'s not possible to get response message since API was not called.')

        '''
        Unfortunately some instances can return valid json with text/html content type. 
        So we're assuming that that case it's not 'not expected error' and in other steps,
        we will try to get proper error message from that json.
        '''
        if self.api_response.headers['Content-Type'].startswith('text/html') and self.api_response.status_code != 200:
            if self.api_response.status_code == 404:
                self.api_result_msg = self.api_unexpected_error_404_msg.format(self.api_response.status_code)
            else:
                self.api_result_msg = self.api_unexpected_error_msg.format(self.api_response.status_code)
        else:
            if self.api_response.status_code == 200:
                if self.api_expected_data_type == self.CONST_EXPECTED_DATA_TYPE_JSON:
                    self.api_response_json = self.get_response_json()
                    if 'response_code' in self.api_response_json:  # Unfortunately not all of endpoints return the unified json.
                        if self.api_response_json['response_code'] == 0:
                            self.api_result_msg = self.api_success_msg
                            self.response_msg_success_nature = True
                        else:
                            self.api_result_msg = self.api_expected_error_msg.format(self.api_response.status_code, self.api_response_json['response_code'], self.api_response_json['response']['error'])
                    else:
                        self.api_result_msg = self.api_success_msg
                        self.response_msg_success_nature = True
                else:  # Few endpoints can return files
                    # Endpoint which is returning file, can also return json file. Then we need to find if we get error msg or that json file.
                    if 'response_code' in self.get_response_json():
                        self.api_result_msg = self.api_expected_error_msg.format(self.api_response.status_code, self.api_response_json['response_code'], self.api_response_json['response']['error'])
                    else:
                        self.api_result_msg = self.api_success_msg
                        self.response_msg_success_nature = True
            else:
                if self.api_expected_data_type == self.CONST_EXPECTED_DATA_TYPE_JSON and bool(self.api_response.json()) is True:  # Sometimes response can has status code different than 200 and store json with error msg
                    self.api_response_json = self.api_response.json()
                    self.api_result_msg = self.api_expected_error_msg.format(self.api_response.status_code, self.api_response_json['response_code'], self.api_response_json['response']['error'])
                else:
                    if self.api_response.status_code == 404:
                        self.api_result_msg = self.api_unexpected_error_404_msg.format(self.api_response.status_code)
                    else:
                        self.api_result_msg = self.api_unexpected_error_msg.format(self.api_response.status_code)

        return self.api_result_msg

    def get_api_response(self):
        if self.api_response is None:
            raise ResponseObjectNotExistError('It\'s not possible to get api response before doing request.')

        return self.api_response

    def get_response_msg_success_nature(self):
        if self.api_response is None:
            raise ResponseObjectNotExistError('It\'s not possible to define api msg nature since API was not called.')

        return self.response_msg_success_nature

    def get_response_status_code(self):
        if self.api_response is None:
            raise ResponseObjectNotExistError('It\'s not possible to get response code since API was not called.')

        return self.api_response.status_code

    def get_prepared_response_msg(self):
        if self.api_result_msg == '':
            self.api_result_msg = self.prepare_response_msg()

        return self.api_result_msg

    def get_response_json(self):
        if self.api_response is None:
            raise ResponseObjectNotExistError('It\'s not possible to get response json since API was not called.')
        elif bool(self.api_response_json) is False:
            try:
                if self.api_response.headers['Content-Type'] == 'application/json':
                    self.api_response_json = self.api_response.json()
                elif self.api_response.headers['Content-Type'].startswith('text/html'):
                    # let's be more tolerant and accept situation when content type is not valid, but response has proper json
                    self.api_response_json = json.loads(self.api_response.text)
                else:
                    '''
                    Some of endpoints can return mixed content type - like file type(success) and json(controlled errors).
                    Let's return there empty dictionary, as it's already properly handled by other project parts.
                    '''
                    self.api_response_json = {}
            except json.decoder.JSONDecodeError:
                '''
                When response has status code equal 200 and we're expecting json, there should be json always.
                Let's ignore other cases as for errors like 404, 500, we're getting html page instead.
                That case should be handled in some other place.
                '''
                if self.get_response_status_code() == 200 and self.request_method_name == self.CONST_EXPECTED_DATA_TYPE_JSON:
                    raise JsonParseError('Failed to parse response: \'{}\''.format(self.api_response.text))
                else:
                    self.api_response_json = {}

        return self.api_response_json

    def build_url(self, params):
        if ':' in self.endpoint_url:
            url_data = params
            url_data_copy = url_data.copy()
            for key, value in url_data.items():
                searched_key = ':' + key
                if searched_key in self.endpoint_url:
                    self.endpoint_url = self.endpoint_url.replace(':' + key, value)
                    del url_data_copy[key]  # Working on copy, since it's not possible to manipulate dict size, during iteration

            if self.request_method_name == self.CONST_REQUEST_METHOD_GET:
                self.params = url_data_copy
            else:
                self.data = url_data_copy

    def get_full_endpoint_url(self):
        return self.server + self.endpoint_url

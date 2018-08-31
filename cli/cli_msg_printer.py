import datetime
import traceback
from colors import Color
import json


class CliMsgPrinter:

    @staticmethod
    def print_call_info(cli_object):
        print(Color.control('Request was sent at ' + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
        print('Endpoint URL: {}'.format(cli_object.api_object.get_full_endpoint_url()))
        print('HTTP Method: {}'.format(cli_object.api_object.request_method_name.upper()))
        print('Sent GET params: {}'.format(cli_object.api_object.params))
        print('Sent POST params: {}'.format(cli_object.api_object.data))
        print('Sent files: {}'.format(cli_object.api_object.files))

    @staticmethod
    def print_error_info(e):
        print(Color.control('During the code execution, error has occurred. Please try again or contact the support.'))
        print(Color.error('Message: \'{}\'.').format(str(e)) + '\n')
        print(traceback.format_exc())

    @staticmethod
    def print_usage_info(api_usage_limits, api_usage, is_api_limit_reached):
        print(Color.control('API Limits for used API Key'))
        print('Webservice API usage limits: {}'.format(api_usage_limits))  # TODO - add submission limits there
        print('Current API usage: {}'.format(json.dumps(api_usage)))
        print('Is limit reached: {}'.format(Color.success('No') if is_api_limit_reached is False else Color.error('Yes')))

    @staticmethod
    def print_api_key_info(current_key_json):
        print(Color.control('Used API Key'))
        print('API Key: {}'.format(current_key_json['api_key']))
        print('Auth Level: {}'.format(current_key_json['auth_level_name']))
        if current_key_json['user'] is not None:
            print('User: {} ({})'.format(current_key_json['user']['name'], current_key_json['user']['email']))


    @staticmethod
    def print_response_summary(arg_iter, iter_cli_object, if_multiple_calls):
        print(Color.control('Received response at ' + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
        print('Response status code: {}'.format(iter_cli_object.get_colored_response_status_code()))
        print('Message: {}'.format(iter_cli_object.get_colored_prepared_response_msg()))
        show_response_msg = 'Showing response'
        if if_multiple_calls is True:
            show_response_msg = '{} for file \'{}\''.format(show_response_msg, arg_iter['file'].name)
        print(Color.control(show_response_msg))

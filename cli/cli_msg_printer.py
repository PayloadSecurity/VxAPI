import datetime
import traceback
from colors import Color
from cli.formatter.cli_limits_formatter import CliLimitsFormatter
import sys


class CliMsgPrinter:

    date_form = '{:%Y-%m-%d %H:%M:%S}'

    @staticmethod
    def print_full_call_info(cli_object):
        print(Color.control('Request was sent at {}'.format(CliMsgPrinter.date_form.format(datetime.datetime.now()))))
        print('Endpoint URL: {}'.format(cli_object.api_object.get_full_endpoint_url()))
        print('HTTP Method: {}'.format(cli_object.api_object.request_method_name.upper()))
        print('Sent GET params: {}'.format(cli_object.api_object.params))
        print('Sent POST params: {}'.format(cli_object.api_object.data))
        print('Sent files: {}'.format(cli_object.api_object.files))

    @staticmethod
    def print_shortest_call_info(cli_object, iteration):
        print(Color.control('Request was sent at {} - {}'.format(CliMsgPrinter.date_form.format(datetime.datetime.now()), iteration)))
        print('Sent files: {}'.format(cli_object.api_object.files))

    @staticmethod
    def print_shorten_call_info(cli_object):
        print(Color.control('Endpoint data which will be reached:'))
        print('Endpoint URL: {}'.format(cli_object.api_object.get_full_endpoint_url()))
        print('HTTP Method: {}'.format(cli_object.api_object.request_method_name.upper()))
        print('Sent GET params: {}'.format(cli_object.api_object.params))
        print('Sent POST params: {}'.format(cli_object.api_object.data))

    @staticmethod
    def print_error_info(e):
        print(Color.control('During the code execution, error has occurred. Please try again or contact the support.'), file=sys.stderr)
        print(Color.error('Message: \'{}\'.').format(str(e)) + '\n', file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)

    @staticmethod
    def print_limits_info(limits_data, limit_type):
        info_container = {
            'query': {
                'title': 'API query limits for used API Key',
                'available': 'Webservice API usage limits: {}',
                'used': 'Current API usage: {}',
            },
            'submission': {
                'title': 'Submission limits for used API Key',
                'available': 'Submission limits: {}',
                'used': 'Used submission limits: {}',
            },
            'quick_scan': {
                'title': 'Quick scan submission limits for used API Key',
                'available': 'Submission limits: {}',
                'used': 'Used submission limits: {}',
            },
        }
        formatted_limits = CliLimitsFormatter.format(limits_data, limit_type)

        texts = info_container[limit_type]

        if formatted_limits:
            print(Color.control(texts['title']))
            print(texts['available'].format(formatted_limits['available']))
            print(texts['used'].format(formatted_limits['used']))
            print('Is limit reached: {}'.format(Color.success('No') if formatted_limits['limit_reached'] is False else Color.error('Yes')))

    @staticmethod
    def print_api_key_info(current_key_json):
        print(Color.control('Used API Key'))
        print('API Key: {}'.format(current_key_json['api_key']))
        print('Auth Level: {}'.format(current_key_json['auth_level_name']))
        if 'user' in current_key_json and current_key_json['user'] is not None:
            print('User: {} ({})'.format(current_key_json['user']['name'], current_key_json['user']['email']))

    @staticmethod
    def print_response_summary(iter_cli_object, iteration=None):
        print(Color.control('Received response at {}{}'.format(CliMsgPrinter.date_form.format(datetime.datetime.now()), '- {}'.format(iteration) if iteration is not None else '')))
        print('Response status code: {}'.format(iter_cli_object.get_colored_response_status_code()))
        print('Message: {}'.format(iter_cli_object.get_colored_prepared_response_msg()))

    @staticmethod
    def print_showing_response(arg_iter, iteration=None):
        show_response_msg = 'Showing response'
        if iteration is not None:
            show_response_msg = '{} for file \'{}\' - {}'.format(show_response_msg, arg_iter['file'] if isinstance(arg_iter['file'], str) else arg_iter['file'].name, iteration)
        print(Color.control(show_response_msg))

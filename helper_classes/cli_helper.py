import datetime
import traceback
from colors import Color
from constants import *


class CliHelper:

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
    def prompt_for_sharing_confirmation(args, instance_url):
        if 'nosharevt' in args:
            if args['nosharevt'] == 'no' and args['quiet'] is False:
                warning_msg = 'You are about to submit your file to all users of {} and the public.'.format(instance_url)
                if 'hybrid-analysis.com' in instance_url:
                    warning_msg += ' Please make sure you consent to the Terms and Conditions of Use and Data Privacy Policy available at: {} and {}.'.format('https://www.hybrid-analysis.com/terms', 'https://www.hybrid-analysis.com/data-protection-policy')
                warning_msg += ' [y/n]'
                submit_warning = input(warning_msg)
                if not submit_warning or submit_warning[0].lower() != 'y':
                    print('You did not indicate approval, exiting ...')
                    exit(1)

    @staticmethod
    def prompt_for_dir_content_submission(args):
        if args['chosen_action'] == ACTION_SUBMIT_FILE:
            number_of_files_to_submit = len(args['file'])
            if args['quiet'] is False and number_of_files_to_submit > 1:
                warning_msg = 'Are you sure that you want to submit the content of selected directory? It contains {} of files. [y/n]'.format(number_of_files_to_submit)
                submit_warning = input(warning_msg)
                if not submit_warning or submit_warning[0].lower() != 'y':
                    print('You did not indicate approval, exiting ...')
                    exit(1)

    @staticmethod
    def check_if_version_is_supported(args, api_instance_version_object, request_handler, headers, minimal_compatible_version):
        if args['quiet'] is False and 'hybrid-analysis.com' not in api_instance_version_object.server:
            api_instance_version_object.call(request_handler, headers)
            api_response = api_instance_version_object.get_api_response()
            if api_response.status_code == 200 and api_instance_version_object.get_response_msg_success_nature() is True:
                if api_instance_version_object.get_response_json()['response']['version'] < minimal_compatible_version:
                    print(Color.warning('This version of VxAPI works best on VxWebService version {} (or above). Consider upgrading to ensure the flawless performance.'.format(minimal_compatible_version)))


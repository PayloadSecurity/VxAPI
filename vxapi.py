#!/usr/bin/env python3
import sys
from sys import platform

try:
    import colorama
    from colorama import init
except ImportError as exc:
    print('\nScript need \'colorama\' module to work. Read README.md to resolve the issue \n')
    exit(1)

if platform == 'win32':
    init()

from colors import Color

if sys.version_info < (3, 4, 0):
    print(Color.error('\nYou need python 3.4 or later to run this script. Possibly you should start the command from calling \'python3\' instead of \'python\'\n'))
    exit(1)

try:
    import requests
except ImportError as exc:
    print(Color.error('\nScript need \'requests\' module to work. Read README.md to resolve the issue \n'))
    exit(1)

try:  # Suppress requests warning connected with disabled verify. Needed only in python 3.5. In python 3.4 that package doesn't exist and message is not visible
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError as exc:
    pass

import argparse

from api_classes.api_submit_url import ApiSubmitUrl
from api_classes.api_submit_file import ApiSubmitFile
from api_classes.api_quota import ApiQuota
from api_classes.api_state import ApiState
from api_classes.api_scan import ApiScan
from api_classes.api_summary import ApiSummary
from api_classes.api_search import ApiSearch
from api_classes.api_relationships import ApiRelationships
from api_classes.api_feed import ApiFeed
from api_classes.api_system_stats import ApiSystemStats
from api_classes.api_system_state import ApiSystemState
from api_classes.api_system_backend import ApiSystemBackend
from api_classes.api_system_queue_size import ApiSystemQueueSize
from api_classes.api_system_in_progress import ApiSystemInProgress
from api_classes.api_system_heartbeat import ApiSystemHeartbeat
from api_classes.api_result import ApiResult
from api_classes.api_result_public import ApiResultPublic
from api_classes.api_reanalyze import ApiReanalyze
from api_classes.api_dropped_file_submit import ApiDroppedFileSubmit
from api_classes.api_sample_dropped_files import ApiSampleDroppedFiles
from api_classes.api_sample_screenshots import ApiSampleScreenshots
from api_classes.api_api_key_data import ApiApiKeyData
from api_classes.api_api_limits import ApiApiLimits

from cli_classes.cli_quota import CliQuota
from cli_classes.cli_state import CliState
from cli_classes.cli_scan import CliScan
from cli_classes.cli_summary import CliSummary
from cli_classes.cli_search import CliSearch
from cli_classes.cli_relationships import CliRelationships
from cli_classes.cli_feed import CliFeed
from cli_classes.cli_system_stats import CliSystemStats
from cli_classes.cli_system_state import CliSystemState
from cli_classes.cli_system_heartbeat import CliSystemHeartbeat
from cli_classes.cli_system_backend import CliSystemBackend
from cli_classes.cli_system_in_progress import CliSystemInProgress
from cli_classes.cli_system_queue_size import CliSystemQueueSize
from cli_classes.cli_result import CliResult
from cli_classes.cli_result_public import CliResultPublic
from cli_classes.cli_submit_file import CliSubmitFile
from cli_classes.cli_submit_url_file import CliSubmitUrlFile
from cli_classes.cli_submit_url import CliSubmitUrl
from cli_classes.cli_reanalyze import CliReanalyze
from cli_classes.cli_dropped_file_submit import CliDroppedFileSubmit
from cli_classes.cli_sample_dropped_files import CliSampleDroppedFiles
from cli_classes.cli_sample_screenshots import CliSampleScreenshots
from cli_classes.cli_api_limits import CliApiLimits

from exceptions import MissingConfigurationError
from exceptions import RetrievingApiKeyDataError
from exceptions import ReachedApiLimitError

import datetime
import os.path
import json

from collections import OrderedDict
from cli_classes.cli_argument_builder import CliArgumentBuilder

from _version import __version__

def main():
    try:
        if os.path.exists('config.py'):
            from config import get_config
            config = get_config()
        else:
            raise MissingConfigurationError('Configuration is missing. Before running CLI, please copy the file \'config_tpl.pl\' from current dir, rename it to \'config.pl\', and fill')
    
        program_name = 'VxWebService Python API Connector'
        program_version = __version__
        vxapi_cli_headers = {'User-agent': 'VxApi CLI Connector'}

        if config['server'].endswith('/'):
            config['server'] = config['server'][:-1]

        map_of_available_actions = OrderedDict([
            ('get_api_limits', CliApiLimits(ApiApiLimits(config['api_key'], config['api_secret'], config['server']))),
            ('get_feed', CliFeed(ApiFeed(config['api_key'], config['api_secret'], config['server']))),
            ('get_relationships', CliRelationships(ApiRelationships(config['api_key'], config['api_secret'], config['server']))),
            ('get_result', CliResult(ApiResult(config['api_key'], config['api_secret'], config['server']))),
            ('get_public_result', CliResultPublic(ApiResultPublic(config['api_key'], config['api_secret'], config['server']))),
            ('get_sample_dropped_files', CliSampleDroppedFiles(ApiSampleDroppedFiles(config['api_key'], config['api_secret'], config['server']))),
            ('get_sample_screenshots', CliSampleScreenshots(ApiSampleScreenshots(config['api_key'], config['api_secret'], config['server']))),
            ('get_scan', CliScan(ApiScan(config['api_key'], config['api_secret'], config['server']))),
            ('get_state', CliState(ApiState(config['api_key'], config['api_secret'], config['server']))),
            ('get_summary', CliSummary(ApiSummary(config['api_key'], config['api_secret'], config['server']))),
            ('get_system_backend', CliSystemBackend(ApiSystemBackend(config['api_key'], config['api_secret'], config['server']))),
            ('get_system_in_progress', CliSystemInProgress(ApiSystemInProgress(config['api_key'], config['api_secret'], config['server']))),
            ('get_system_heartbeat', CliSystemHeartbeat(ApiSystemHeartbeat(config['api_key'], config['api_secret'], config['server']))),
            ('get_system_state', CliSystemState(ApiSystemState(config['api_key'], config['api_secret'], config['server']))),
            ('get_system_stats', CliSystemStats(ApiSystemStats(config['api_key'], config['api_secret'], config['server']))),
            ('get_system_queue_size', CliSystemQueueSize(ApiSystemQueueSize(config['api_key'], config['api_secret'], config['server']))),
            ('get_quota', CliQuota(ApiQuota(config['api_key'], config['api_secret'], config['server']))),
            ('reanalyze_sample', CliReanalyze(ApiReanalyze(config['api_key'], config['api_secret'], config['server']))),
            ('search', CliSearch(ApiSearch(config['api_key'], config['api_secret'], config['server']))),
            ('submit_dropped_file', CliDroppedFileSubmit(ApiDroppedFileSubmit(config['api_key'], config['api_secret'], config['server']))),
            ('submit_file', CliSubmitFile(ApiSubmitFile(config['api_key'], config['api_secret'], config['server']))),
            ('submit_url_file', CliSubmitUrlFile(ApiSubmitFile(config['api_key'], config['api_secret'], config['server']))),
            ('submit_url', CliSubmitUrl(ApiSubmitUrl(config['api_key'], config['api_secret'], config['server']))),
        ])

        request_session = requests.Session()

        api_object_api_key_data = ApiApiKeyData(config['api_key'], config['api_secret'], config['server'])
        api_object_api_key_data.call(request_session, vxapi_cli_headers)
        if api_object_api_key_data.get_response_status_code() != 200 or api_object_api_key_data.get_response_json()['response_code'] != 0:
            raise RetrievingApiKeyDataError('Can\'t retrieve data for api_key \'{}\' in the webservice: \'{}\'. Response status code: \'{}\''.format(config['api_key'], config['server'], api_object_api_key_data.get_response_status_code()))

        used_api_key_data = api_object_api_key_data.get_response_json()['response']
        parser = argparse.ArgumentParser(description=program_name, formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)
        parser.add_argument('--version', '-ver', action='version', version='{} - version {}'.format(program_name, program_version))
        CliArgumentBuilder(parser).add_help_argument()
    
        subparsers = parser.add_subparsers(help='Action names for \'{}\' auth level'.format(used_api_key_data['auth_level_name']), dest="chosen_action")
    
        for name, cli_object in map_of_available_actions.items():
            if cli_object.api_object.endpoint_auth_level <= used_api_key_data['auth_level']:
                child_parser = subparsers.add_parser(name=name, help=cli_object.help_description, add_help=False)
                cli_object.add_parser_args(child_parser)
    
        args = vars(parser.parse_args())

        if args['chosen_action'] is not None:
            cli_object = map_of_available_actions[args['chosen_action']]
            cli_object.attach_args(args)
            if args['verbose'] is True:
                cli_object.init_verbose_mode()
                print(Color.control('Running \'{}\' in version \'{}\''.format(program_name, program_version)))

                if args['chosen_action'] != 'get_api_limits':
                    # API limits checking should be done here, to ensure that user always will be able to run command in help mode. Also there is no need to run it in non verbose mode.
                    api_object_api_limits = ApiApiLimits(config['api_key'], config['api_secret'], config['server'])
                    api_object_api_limits.call(request_session, vxapi_cli_headers)
                    api_limits_response_json = api_object_api_limits.get_response_json()

                    # Ignore when WebService doesn't have that endpoint
                    if api_object_api_limits.get_response_status_code() != 404:
                        if api_object_api_limits.get_response_status_code() != 200 or api_limits_response_json['response_code'] == -1:
                            raise RetrievingApiKeyDataError('Can\'t check API limits before calling requested endpoint in webservice: \'{}\'. Response status code: \'{}\''.format(config['server'], api_object_api_limits.get_response_status_code()))

                        if api_object_api_limits.get_response_status_code() == 200 and api_limits_response_json['response_code'] == 0 and api_limits_response_json['response']['limit_reached'] is True:
                            name_of_reached_limit = api_limits_response_json['response']['name_of_reached_limit']
                            raise ReachedApiLimitError('Exceeded maximum API requests per {}({}). Please try again later.'.format(name_of_reached_limit, api_limits_response_json['response']['used'][name_of_reached_limit]))

                    if api_object_api_limits.get_response_status_code() == 200 and api_limits_response_json['response_code'] == 0:
                        api_usage = OrderedDict()
                        api_usage_limits = api_limits_response_json['response']['limits']
                        is_api_limit_reached = False

                        for period, used_limit in api_limits_response_json['response']['used'].items():
                            # Given request is made after checking api limits. It means that we have to add 1 to current limits, to simulate that what happen after making requested API call
                            api_usage[period] = used_limit + 1
                            if is_api_limit_reached is False and api_usage[period] == api_usage_limits[period]:
                                is_api_limit_reached = True

                        print(Color.control('API Limits for used API Key'))
                        print('Webservice API usage limits: {}'.format(api_usage_limits))
                        print('Current API usage: {}'.format(json.dumps(api_usage)))
                        print('Is limit reached: {}'.format(Color.success('No') if is_api_limit_reached is False else Color.error('Yes')))

                print(Color.control('Used API Key'))
                print('API Key: {}'.format(used_api_key_data['api_key']))
                print('Auth Level: {}'.format(used_api_key_data['auth_level_name']))
                if used_api_key_data['user'] is not None:
                    print('User: {} ({})'.format(used_api_key_data['user']['name'], used_api_key_data['user']['email']))

                print(Color.control('Request was sent at ' + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
                print('Endpoint URL: {}'.format(cli_object.api_object.get_full_endpoint_url()))
                print('HTTP Method: {}'.format(cli_object.api_object.request_method_name.upper()))
                print('Sent GET params: {}'.format(cli_object.api_object.params))
                print('Sent POST params: {}'.format(cli_object.api_object.data))
                print('Sent files: {}'.format(cli_object.api_object.files))

            cli_object.api_object.call(request_session, vxapi_cli_headers)
            if args['verbose'] is True:
                print(Color.control('Received response at ' + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
                print('Response status code: {}'.format(cli_object.get_colored_response_status_code()))
                print('Message: {}'.format(cli_object.get_colored_prepared_response_msg()))
                print(Color.control('Showing response'))

            print(cli_object.get_result_msg())
            cli_object.do_post_processing()

            if args['verbose'] is True:
                print('\n')
        else:
            print(Color.control('No option was selected. To check CLI options, run script in help mode: \'{} -h\''.format(__file__)))
    except Exception as exc:
        print(Color.control('During the code execution, error has occurred. Please try again or contact the support.'))
        print(Color.error('Message: \'{}\'.').format(str(exc)) + '\n')

if __name__ == "__main__":
    main()


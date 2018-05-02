#!/usr/bin/env python3
import sys
import traceback

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

from constants import *
from api_classes.api_submit_url import ApiSubmitUrl
from api_classes.api_submit_file import ApiSubmitFile
from api_classes.api_api_submission_limits import ApiApiSubmissionLimits
from api_classes.api_state import ApiState
from api_classes.api_scan import ApiScan
from api_classes.api_bulk_scan import ApiBulkScan
from api_classes.api_summary import ApiSummary
from api_classes.api_bulk_summary import ApiBulkSummary
from api_classes.api_search import ApiSearch
from api_classes.api_relationships import ApiRelationships
from api_classes.api_feed import ApiFeed
from api_classes.api_nssf_download import ApiNssfDownload
from api_classes.api_nssf_list import ApiNssfList
from api_classes.api_system_stats import ApiSystemStats
from api_classes.api_system_state import ApiSystemState
from api_classes.api_system_backend import ApiSystemBackend
from api_classes.api_system_queue_size import ApiSystemQueueSize
from api_classes.api_system_in_progress import ApiSystemInProgress
from api_classes.api_system_heartbeat import ApiSystemHeartbeat
from api_classes.api_result import ApiResult
from api_classes.api_reanalyze import ApiReanalyze
from api_classes.api_dropped_file_submit import ApiDroppedFileSubmit
from api_classes.api_sample_dropped_files import ApiSampleDroppedFiles
from api_classes.api_sample_screenshots import ApiSampleScreenshots
from api_classes.api_api_key_data import ApiApiKeyData
from api_classes.api_api_query_limits import ApiApiQueryLimits
from api_classes.api_api_limits_summary import ApiApiLimitsSummary
from api_classes.api_environments import ApiEnvironments
from api_classes.api_url_hash import ApiUrlHash
from api_classes.api_instance_version import ApiInstanceVersion

from cli_classes.cli_api_submission_limits import CliApiSubmissionLimits
from cli_classes.cli_api_limits_summary import CliApiLimitsSummary
from cli_classes.cli_state import CliState
from cli_classes.cli_scan import CliScan
from cli_classes.cli_bulk_scan import CliBulkScan
from cli_classes.cli_summary import CliSummary
from cli_classes.cli_bulk_summary import CliBulkSummary
from cli_classes.cli_search import CliSearch
from cli_classes.cli_relationships import CliRelationships
from cli_classes.cli_feed import CliFeed
from cli_classes.cli_nssf_download import CliNssfDownload
from cli_classes.cli_nssf_list import CliNssfList
from cli_classes.cli_system_stats import CliSystemStats
from cli_classes.cli_system_state import CliSystemState
from cli_classes.cli_system_heartbeat import CliSystemHeartbeat
from cli_classes.cli_system_backend import CliSystemBackend
from cli_classes.cli_system_in_progress import CliSystemInProgress
from cli_classes.cli_system_queue_size import CliSystemQueueSize
from cli_classes.cli_result import CliResult
from cli_classes.cli_submit_file import CliSubmitFile
from cli_classes.cli_submit_url_file import CliSubmitUrlFile
from cli_classes.cli_submit_url import CliSubmitUrl
from cli_classes.cli_reanalyze import CliReanalyze
from cli_classes.cli_dropped_file_submit import CliDroppedFileSubmit
from cli_classes.cli_sample_dropped_files import CliSampleDroppedFiles
from cli_classes.cli_sample_screenshots import CliSampleScreenshots
from cli_classes.cli_api_query_limits import CliApiQueryLimits
from cli_classes.cli_environments import CliEnvironments
from cli_classes.cli_url_hash import CliUrlHash

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
            raise MissingConfigurationError('Configuration is missing. Before running CLI, please copy the file \'config_tpl.py\' from current dir, rename it to \'config.py\', and fill')

        program_name = 'VxWebService Python API Connector'
        program_version = __version__
        vxapi_cli_headers = {'User-agent': 'VxApi CLI Connector'}

        if config['server'].endswith('/'):
            config['server'] = config['server'][:-1]

        if config['server'].endswith('vxstream-sandbox.com'):
            config['server'] = config['server'].replace('vxstream-sandbox.com', 'falcon-sandbox.com')

        map_of_available_actions = OrderedDict([
            (ACTION_GET_API_LIMITS, CliApiLimitsSummary(ApiApiLimitsSummary(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_API_QUERY_LIMITS, CliApiQueryLimits(ApiApiQueryLimits(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_API_SUBMISSION_LIMITS, CliApiSubmissionLimits(ApiApiSubmissionLimits(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_ENVIRONMENTS, CliEnvironments(ApiEnvironments(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_FEED, CliFeed(ApiFeed(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_NSSF_FILES, CliNssfDownload(ApiNssfDownload(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_NSSF_LIST, CliNssfList(ApiNssfList(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_RELATIONSHIPS, CliRelationships(ApiRelationships(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_RESULT, CliResult(ApiResult(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_SAMPLE_DROPPED_FILES, CliSampleDroppedFiles(ApiSampleDroppedFiles(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_SAMPLE_SCREENSHOTS, CliSampleScreenshots(ApiSampleScreenshots(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_SCAN, CliScan(ApiScan(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_BULK_SCAN, CliBulkScan(ApiBulkScan(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_STATE, CliState(ApiState(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_SUMMARY, CliSummary(ApiSummary(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_BULK_SUMMARY, CliBulkSummary(ApiBulkSummary(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_SYSTEM_BACKEND, CliSystemBackend(ApiSystemBackend(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_SYSTEM_IN_PROGRESS, CliSystemInProgress(ApiSystemInProgress(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_SYSTEM_HEARTBEAT, CliSystemHeartbeat(ApiSystemHeartbeat(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_SYSTEM_STATE, CliSystemState(ApiSystemState(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_SYSTEM_STATS, CliSystemStats(ApiSystemStats(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_SYSTEM_QUEUE_SIZE, CliSystemQueueSize(ApiSystemQueueSize(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_GET_URL_HASH, CliUrlHash(ApiUrlHash(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_REANALYZE_SAMPLE, CliReanalyze(ApiReanalyze(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_SEARCH, CliSearch(ApiSearch(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_SUBMIT_DROPPED_FILE, CliDroppedFileSubmit(ApiDroppedFileSubmit(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_SUBMIT_FILE, CliSubmitFile(ApiSubmitFile(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_SUBMIT_URL_FILE, CliSubmitUrlFile(ApiSubmitFile(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_SUBMIT_URL, CliSubmitUrl(ApiSubmitUrl(config['api_key'], config['api_secret'], config['server']))),
        ])


        request_session = requests.Session()

        api_object_api_key_data = ApiApiKeyData(config['api_key'], config['api_secret'], config['server'])
        api_object_api_key_data.call(request_session, vxapi_cli_headers)
        api_key_data_json_response = api_object_api_key_data.get_response_json()

        if api_object_api_key_data.get_response_status_code() != 200 or api_key_data_json_response['response_code'] != 0:
            base_error_message = 'Can\'t retrieve data for given API Key \'{}\' in the webservice: \'{}\'. Response status code: \'{}\''.format(config['api_key'], config['server'], api_object_api_key_data.get_response_status_code())
            if 'response' in api_key_data_json_response and 'error' in api_key_data_json_response['response']:
                base_error_message += '. Response message: \'{}\''.format(api_key_data_json_response['response']['error'])

            raise RetrievingApiKeyDataError(base_error_message)

        used_api_key_data = api_key_data_json_response['response']
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
                cli_object.prompt_for_sharing_confirmation(config['server'])
                cli_object.check_if_version_is_supported(ApiInstanceVersion(config['api_key'], config['api_secret'], config['server']), request_session,vxapi_cli_headers, MINIMAL_SUPPORTED_INSTANCE_VERSION)

                if args['chosen_action'] != 'get_api_limits':
                    # API limits checking should be done here, to ensure that user always will be able to run command in help mode. Also there is no need to run it in non verbose mode.
                    api_object_api_limits = ApiApiQueryLimits(config['api_key'], config['api_secret'], config['server'])
                    api_object_api_limits.call(request_session, vxapi_cli_headers)
                    api_limits_response_json = api_object_api_limits.get_response_json()

                    # Ignore when WebService doesn't have that endpoint
                    if api_object_api_limits.get_response_status_code() != 404:
                        if api_object_api_limits.get_response_status_code() != 200 or api_limits_response_json['response_code'] == -1:
                            raise RetrievingApiKeyDataError('Can\'t check API limits before calling requested endpoint in webservice: \'{}\'. Response status code: \'{}\''.format(config['server'], api_object_api_limits.get_response_status_code()))

                        if api_object_api_limits.get_response_status_code() == 200 and api_limits_response_json['response_code'] == 0 and api_limits_response_json['response']['limit_reached'] is True:
                            name_of_reached_limit = api_limits_response_json['response']['name_of_reached_limit']
                            raise ReachedApiLimitError('Exceeded maximum API requests per {}({}). Please try again later.'.format(name_of_reached_limit, api_limits_response_json['response']['used'][name_of_reached_limit]))

                    if api_object_api_limits.get_response_status_code() == 200 and api_limits_response_json['response_code'] == 0 and api_limits_response_json['response']['used']:
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
            else:
                cli_object.prompt_for_sharing_confirmation(config['server'])
                cli_object.check_if_version_is_supported(ApiInstanceVersion(config['api_key'], config['api_secret'], config['server']), request_session,vxapi_cli_headers, MINIMAL_SUPPORTED_INSTANCE_VERSION)

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
        print(traceback.format_exc())

if __name__ == "__main__":
    main()


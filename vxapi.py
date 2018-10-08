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
import logging

from constants import *
from exceptions import *

import datetime
import os.path
import json

from collections import OrderedDict
# import cli.arguments_builders

from api.callers.api_caller import ApiCaller

from api.callers.search import *
from cli.wrappers.search import *

from api.callers.key import *
from cli.wrappers.key import *

from api.callers.overview import *
from cli.wrappers.overview import *

from api.callers.submit import *
from cli.wrappers.submit import *

from api.callers.report import *
from cli.wrappers.report import *

from cli.arguments_builders import *

from cli.cli_helper import CliHelper
from cli.cli_msg_printer import CliMsgPrinter
from cli.cli_prompts import CliPrompts

from _version import __version__

from copy import copy, deepcopy

# os.environ['APP_ENV'] = 'test'
# os.environ['TEST_CONFIG'] = json.dumps({
#         'api_key': 'test_me_please',
#         'server': 'mock://my-webservice-instance'
# })
# os.environ['TEST_SCENARIO'] = '1'


is_test_env = True if 'APP_ENV' in os.environ and os.environ['APP_ENV'] == 'test' else False

if is_test_env is True:
    import requests_mock


class CliManager:

    config = None
    program_name = 'VxWebService Python API Connector'
    program_version = __version__
    vxapi_cli_headers = {'User-agent': 'VxApi CLI Connector'}
    request_session = None

    def load_config(self):
        if is_test_env is True:
            config = json.loads(os.environ['TEST_CONFIG'])
        elif os.path.exists('config.py'):
            from config import get_config
            config = get_config()
        else:
            raise MissingConfigurationError('Configuration is missing. Before running CLI, please copy the file \'config_tpl.py\' from current dir, rename it to \'config.py\', and fill')

        if config['server'].endswith('/'):
            config['server'] = config['server'][:-1]

        if config['server'].endswith('vxstream-sandbox.com'):
            config['server'] = config['server'].replace('vxstream-sandbox.com', 'falcon-sandbox.com')

        self.config = config

        return self.config

    def prepare_test_env(self):
        if is_test_env is True:
            adapter = requests_mock.Adapter()

            imported_scenarios = __import__('tests._requests_scenarios.{}'.format(os.environ['TEST_SCENARIO']), fromlist=[None])

            for scenario in imported_scenarios.scenarios:
                scenario['url'] = '{}/api/v2{}'.format(self.config['server'], scenario['url'])
                if 'headers' in scenario:
                    if 'api-limits' in scenario['headers']:
                        scenario['headers']['api-limits'] = json.dumps(scenario['headers']['api-limits'])

                    if 'submission-limits' in scenario['headers']:
                        scenario['headers']['submission-limits'] = json.dumps(scenario['headers']['submission-limits'])

                adapter.register_uri(**scenario)

            self.request_session.mount('mock', adapter)

    def get_map_of_available_actions(self):
        config = self.config

        return OrderedDict([
            # (ACTION_GET_API_LIMITS, CliApiLimitsSummary(ApiApiLimitsSummary(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_API_QUERY_LIMITS, CliApiQueryLimits(ApiApiQueryLimits(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_API_SUBMISSION_LIMITS, CliApiSubmissionLimits(ApiApiSubmissionLimits(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_ENVIRONMENTS, CliEnvironments(ApiEnvironments(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_FEED, CliFeed(ApiFeed(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_NSSF_FILES, CliNssfDownload(ApiNssfDownload(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_NSSF_LIST, CliNssfList(ApiNssfList(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_RELATIONSHIPS, CliRelationships(ApiRelationships(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_RESULT, CliResult(ApiResult(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SAMPLE_DROPPED_FILES, CliSampleDroppedFiles(ApiSampleDroppedFiles(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SAMPLE_SCREENSHOTS, CliSampleScreenshots(ApiSampleScreenshots(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SCAN, CliScan(ApiScan(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_BULK_SCAN, CliBulkScan(ApiBulkScan(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_STATE, CliState(ApiState(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SUMMARY, CliSummary(ApiSummary(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_BULK_SUMMARY, CliBulkSummary(ApiBulkSummary(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SYSTEM_BACKEND, CliSystemBackend(ApiSystemBackend(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SYSTEM_IN_PROGRESS, CliSystemInProgress(ApiSystemInProgress(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SYSTEM_HEARTBEAT, CliSystemHeartbeat(ApiSystemHeartbeat(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SYSTEM_STATE, CliSystemState(ApiSystemState(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SYSTEM_STATS, CliSystemStats(ApiSystemStats(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_SYSTEM_QUEUE_SIZE, CliSystemQueueSize(ApiSystemQueueSize(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_GET_URL_HASH, CliUrlHash(ApiUrlHash(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_REANALYZE_SAMPLE, CliReanalyze(ApiReanalyze(config['api_key'], config['api_secret'], config['server']))),
            (ACTION_SEARCH_HASH, CliSearchHash(ApiSearchHash(config['api_key'], config['server']), ACTION_SEARCH_HASH)),
            (ACTION_SEARCH_HASHES, CliSearchHashes(ApiSearchHashes(config['api_key'], config['server']), ACTION_SEARCH_HASHES)),
            (ACTION_SEARCH_STATES, CliSearchStates(ApiSearchStates(config['api_key'], config['server']), ACTION_SEARCH_STATES)),
            (ACTION_SEARCH_TERMS, CliSearchTerms(ApiSearchTerms(config['api_key'], config['server']), ACTION_SEARCH_TERMS)),
            (ACTION_GET_OVERVIEW, CliOverview(ApiOverview(config['api_key'], config['server']), ACTION_GET_OVERVIEW)),
            (ACTION_GET_REFRESHED_OVERVIEW, CliOverviewRefresh(ApiOverviewRefresh(config['api_key'], config['server']), ACTION_GET_REFRESHED_OVERVIEW)),
            (ACTION_GET_OVERVIEW_SUMMARY, CliOverviewSummary(ApiOverviewSummary(config['api_key'], config['server']), ACTION_GET_OVERVIEW_SUMMARY)),
            (ACTION_GET_OVERVIEW_SAMPLE, CliOverviewSample(ApiOverviewSample(config['api_key'], config['server']), ACTION_GET_OVERVIEW_SAMPLE)),
            (ACTION_SUBMIT_DROPPED_FILE, CliSubmitDroppedFile(ApiSubmitDroppedFile(config['api_key'], config['server']), ACTION_SUBMIT_DROPPED_FILE)),
            (ACTION_SUBMIT_FILE, CliSubmitFile(ApiSubmitFile(config['api_key'], config['server']), ACTION_SUBMIT_FILE)),
            (ACTION_SUBMIT_HASH_FOR_URL, CliSubmitHashForUrl(ApiSubmitHashForUrl(config['api_key'], config['server']), ACTION_SUBMIT_HASH_FOR_URL)),
            (ACTION_SUBMIT_REANALYZE, CliSubmitReanalyze(ApiSubmitReanalyze(config['api_key'], config['server']), ACTION_SUBMIT_REANALYZE)),
            (ACTION_SUBMIT_URL_FOR_ANALYSIS, CliSubmitUrlForAnalysis(ApiSubmitUrlForAnalysis(config['api_key'], config['server']), ACTION_SUBMIT_URL_FOR_ANALYSIS)),
            (ACTION_SUBMIT_URL_TO_FILE, CliSubmitUrlToFile(ApiSubmitUrlToFile(config['api_key'], config['server']), ACTION_SUBMIT_URL_TO_FILE)),
            (ACTION_REPORT_GET_BULK_SUMMARY, CliReportBulkSummary(ApiReportBulkSummary(config['api_key'], config['server']), ACTION_REPORT_GET_BULK_SUMMARY)),
            (ACTION_REPORT_GET_BULK_DEMO, CliReportDemoBulk(ApiReportDemoBulk(config['api_key'], config['server']), ACTION_REPORT_GET_BULK_DEMO)),
            (ACTION_REPORT_GET_DROPPED_FILE_RAW, CliReportDroppedFileRaw(ApiReportDroppedFileRaw(config['api_key'], config['server']), ACTION_REPORT_GET_DROPPED_FILE_RAW)),
            (ACTION_REPORT_GET_DROPPED_FILES, CliReportDroppedFiles(ApiReportDroppedFiles(config['api_key'], config['server']), ACTION_REPORT_GET_DROPPED_FILES)),
            (ACTION_REPORT_GET_SUMMARY, CliReportSummary(ApiReportSummary(config['api_key'], config['server']), ACTION_REPORT_GET_SUMMARY)),
            (ACTION_REPORT_GET_ENHANCED_SUMMARY, CliReportEnhancedSummary(ApiReportEnhancedSummary(config['api_key'], config['server']), ACTION_REPORT_GET_ENHANCED_SUMMARY)),
            (ACTION_REPORT_GET_FILE, CliReportFile(ApiReportFile(config['api_key'], config['server']), ACTION_REPORT_GET_FILE)),
            (ACTION_REPORT_GET_SCREENSHOTS, CliReportScreenshots(ApiReportScreenshots(config['api_key'], config['server']), ACTION_REPORT_GET_SCREENSHOTS)),
            (ACTION_REPORT_GET_STATE, CliReportState(ApiReportState(config['api_key'], config['server']), ACTION_REPORT_GET_STATE)),
            # (ACTION_SEARCH_HASHES, CliSearch(ApiSearch(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_SEARCH_STATES, CliSearch(ApiSearch(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_SEARCH_TERMS, CliSearch(ApiSearch(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_SUBMIT_DROPPED_FILE, CliDroppedFileSubmit(ApiDroppedFileSubmit(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_SUBMIT_FILE, CliSubmitFile(ApiSubmitFile(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_SUBMIT_URL_FILE, CliSubmitUrlFile(ApiSubmitFile(config['api_key'], config['api_secret'], config['server']))),
            # (ACTION_SUBMIT_URL, CliSubmitUrl(ApiSubmitUrl(config['api_key'], config['api_secret'], config['server']))),
        ])

    def check_current_key(self):
        config = self.config
        
        api_object_key_current = ApiKeyCurrent(config['api_key'], config['server'])
        api_object_key_current.call(self.request_session, self.vxapi_cli_headers)
        api_key_data_json_response = api_object_key_current.get_response_json()

        if api_object_key_current.get_response_status_code() != 200 or bool(api_key_data_json_response) is False:
            base_error_message = 'Can\'t retrieve _data for given API Key \'{}\' in the webservice: \'{}\'. Response status code: \'{}\''.format(config['api_key'], config['server'], api_object_key_current.get_response_status_code())
            if 'message' in api_key_data_json_response:
                base_error_message += '. Response message: \'{}\''.format(api_key_data_json_response['message'])

            raise RetrievingApiKeyDataError(base_error_message)
        
        return api_object_key_current
    
    def prepare_parser(self, current_key_json, map_of_available_actions):
        parser = argparse.ArgumentParser(description=self.program_name, formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)
        parser.add_argument('--version', '-ver', action='version', version='{} - version {}'.format(self.program_name, self.program_version))
        DefaultCliArguments(parser).add_help_argument()

        subparsers = parser.add_subparsers(help='Action names for \'{}\' auth level'.format(current_key_json['auth_level_name']), dest="chosen_action")

        for name, cli_object in map_of_available_actions.items():
            if cli_object.api_object.endpoint_auth_level <= current_key_json['auth_level']:
                child_parser = subparsers.add_parser(name=name, help=cli_object.help_description, add_help=False)
                cli_object.add_parser_args(child_parser)
        
        return parser

    def prepare_args_iterations(self, args):
        args_iterations = []
        if args['chosen_action'] == ACTION_SUBMIT_FILE:
            for file in args['file']:
                arg_iter = args.copy()
                arg_iter['file'] = file
                args_iterations.append(arg_iter)
        else:
            args_iterations = [args]
            
        return args_iterations

    def prepare_api_usage_data(self, api_limits):
        api_usage = OrderedDict()
        api_usage_limits = api_limits['limits']
        is_api_limit_reached = False

        for period, used_limit in api_limits['used'].items():
            # Given request is made after checking api limits. It means that we have to add 1 to current limits, to simulate that what happen after making requested API call TODO - check that logic
            api_usage[period] = used_limit + 1
            if is_api_limit_reached is False and api_usage[period] == api_usage_limits[period]:
                is_api_limit_reached = True

        return {'api_usage_limits': api_usage_limits, 'api_usage': api_usage, 'is_api_limit_reached': is_api_limit_reached}

    def rebuild_args(self, args):
        rebuilt_args = {}
        for key, value in args.items():
            rebuilt_args[key.replace('-', '_')] = value

        return rebuilt_args

    def run(self):
        self.request_session = requests.Session()
        self.load_config()
        self.prepare_test_env()
        
        map_of_available_actions = self.get_map_of_available_actions()
        current_key_api_object = self.check_current_key()
        current_key_json = current_key_api_object.get_response_json()
        current_key_response_headers = current_key_api_object.get_headers()
        
        parser = self.prepare_parser(current_key_json, map_of_available_actions)
        args = self.rebuild_args(vars(parser.parse_args()))

        if args['chosen_action'] is not None:
            args_iterations = self.prepare_args_iterations(args)
            if_multiple_calls = True if args['chosen_action'] == ACTION_SUBMIT_FILE and len(args['file']) > 1 else False
            cli_object = map_of_available_actions[args['chosen_action']]

            if args['verbose'] is True:
                cli_object.init_verbose_mode()
                start_msg = 'Running \'{}\' in version \'{}\'. Webservice version: \'{}\', API version: \'{}\''.format(self.program_name, self.program_version, current_key_response_headers['Webservice-Version'], current_key_response_headers['Api-Version'])
                print(Color.control(start_msg))

            CliPrompts.prompt_for_dir_content_submission(args)
            CliPrompts.prompt_for_sharing_confirmation(args, self.config['server'])
            CliHelper.check_if_version_is_supported(args, current_key_response_headers['Webservice-Version'], self.config['server'])
            submission_limits = json.loads(current_key_response_headers['Submission-Limits']) if 'Submission-Limits' in current_key_response_headers else {}
            api_limits = json.loads(current_key_response_headers['Api-Limits'])

            for index, arg_iter in enumerate(args_iterations):
                iter_cli_object = deepcopy(cli_object)
                iter_cli_object.attach_args(arg_iter)

                if api_limits and api_limits['limit_reached'] is True:
                    raise ReachedApiLimitError('Exceeded maximum API requests per {}({}). Please try again later.'.format(api_limits['name_of_reached_limit'], api_limits['used'][api_limits['name_of_reached_limit']]))

                if arg_iter['verbose'] is True:
                    if arg_iter['chosen_action'] != ACTION_GET_API_LIMITS and (if_multiple_calls is False or index == 0) and 'used' in api_limits:
                        CliMsgPrinter.print_usage_info(**self.prepare_api_usage_data(api_limits))

                    if if_multiple_calls is False or index == 0:
                        CliMsgPrinter.print_api_key_info(current_key_json)

                    if arg_iter['chosen_action'] == ACTION_SUBMIT_FILE:
                        if if_multiple_calls is True and index == 0:
                            print(Color.control('Starting the process of sending multiple files ...'))

                        iter_cli_object.attach_file(arg_iter['file'])

                    CliMsgPrinter.print_call_info(iter_cli_object)
                elif arg_iter['chosen_action'] == ACTION_SUBMIT_FILE:
                    iter_cli_object.attach_file(arg_iter['file'])

                try:
                    iter_cli_object.api_object.call(self.request_session, self.vxapi_cli_headers)
                except Exception as e:
                    if if_multiple_calls is True:
                        CliMsgPrinter.print_error_info(e)
                    else:
                        raise e

                if arg_iter['verbose'] is True:
                    CliMsgPrinter.print_response_summary(arg_iter, iter_cli_object, if_multiple_calls)
                elif if_multiple_calls:
                    print(Color.control(arg_iter['file'].name))

                print(iter_cli_object.get_result_msg())

                if iter_cli_object.api_object.if_request_success() is False and if_multiple_calls is True and iter_cli_object.api_object.api_expected_data_type == ApiCaller.CONST_EXPECTED_DATA_TYPE_JSON:
                    response_json = iter_cli_object.api_object.get_response_json()
                    if 'response_code' in response_json and 'Exceeded maximum API requests' in response_json['response']['error']:
                        raise Exception('Requests exceeded maximum API requests, the rest of the unsubmitted files won\'t be processed, exiting ...')
                iter_cli_object.do_post_processing()

                if arg_iter['verbose'] is True:
                    print('\n')
        else:
            print(Color.control('No option was selected. To check CLI options, run script in help mode: \'{} -h\''.format(__file__)))


def main():

    try:
        # TODO - test the moment when some file privileges are missing....
        # logging.basicConfig(filename='cli.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
        # logging.debug('This message should go to the log file')
        # logging.info('So should this')
        # logging.warning('And this, too')
        cli_manager = CliManager()
        cli_manager.run()

    except Exception as e:
        CliMsgPrinter.print_error_info(e)
        sys.exit(1)

if __name__ == "__main__":
    main()


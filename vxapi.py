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

from api.callers.system import *
from cli.wrappers.system import *

from api.callers.feed import *
from cli.wrappers.feed import *

from api.callers.scan import *
from cli.wrappers.scan import *

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
    program_version = __version__
    program_name = 'VxWebService Python API Connector'
    vxapi_cli_headers = {'User-agent': 'VxApi CLI Connector'}
    request_session = None
    loaded_action = None

    def load_config(self):
        if is_test_env is True:
            config = json.loads(os.environ['TEST_CONFIG'])
        elif os.path.exists('config.py'):
            from config import get_config
            config = get_config()
        else:
            raise MissingConfigurationError('Configuration is missing. Before running CLI, please copy the file \'config_tpl.py\' from current dir, rename it to \'config.py\', and fill')

        if 'server' not in config or 'api_key' not in config:
            raise ConfigError('Config does not contain all of required \'server\' and \'api_key\' keys')

        if not config['server'] or not config['api_key']:
            raise ConfigError('Not all of required config keys(\'server\', \'api_key\') contain values')

        if config['server'].endswith('/'):
            config['server'] = config['server'][:-1]

        if config['server'].endswith('vxstream-sandbox.com'):
            config['server'] = config['server'].replace('vxstream-sandbox.com', 'falcon-sandbox.com')

        if len(config['api_key']) < 60:
            raise ConfigError('Your API Key is not compatible with API v2. Please regenerate it at your profile page or create the new one.')

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
            (ACTION_CHECK_LIMITS, {'help_description': 'Return all limits data', 'parser_handler': lambda parser: (DefaultCliArguments(parser)).add_help_opt().add_verbose_arg() }),

            (ACTION_FEED, CliFeed(ApiFeed(config['api_key'], config['server']), ACTION_FEED)),
            (ACTION_FEED_LATEST, CliFeedLatest(ApiFeedLatest(config['api_key'], config['server']), ACTION_FEED_LATEST)),

            (ACTION_KEY_CREATE, CliKeyCreate(ApiKeyCreate(config['api_key'], config['server']), ACTION_KEY_CREATE)),
            (ACTION_KEY_CURRENT, CliKeyCurrent(ApiKeyCurrent(config['api_key'], config['server']), ACTION_KEY_CURRENT)),

            (ACTION_OVERVIEW_GET, CliOverview(ApiOverview(config['api_key'], config['server']), ACTION_OVERVIEW_GET)),
            (ACTION_OVERVIEW_GET_SAMPLE, CliOverviewSample(ApiOverviewSample(config['api_key'], config['server']), ACTION_OVERVIEW_GET_SAMPLE)),
            (ACTION_OVERVIEW_GET_SUMMARY, CliOverviewSummary(ApiOverviewSummary(config['api_key'], config['server']), ACTION_OVERVIEW_GET_SUMMARY)),
            (ACTION_OVERVIEW_REFRESH, CliOverviewRefresh(ApiOverviewRefresh(config['api_key'], config['server']), ACTION_OVERVIEW_REFRESH)),

            (ACTION_REPORT_GET_BULK_DEMO, CliReportDemoBulk(ApiReportDemoBulk(config['api_key'], config['server']), ACTION_REPORT_GET_BULK_DEMO)),
            (ACTION_REPORT_GET_BULK_SUMMARY, CliReportBulkSummary(ApiReportBulkSummary(config['api_key'], config['server']), ACTION_REPORT_GET_BULK_SUMMARY)),
            (ACTION_REPORT_GET_DROPPED_FILES, CliReportDroppedFiles(ApiReportDroppedFiles(config['api_key'], config['server']), ACTION_REPORT_GET_DROPPED_FILES)),
            (ACTION_REPORT_GET_DROPPED_FILE_RAW, CliReportDroppedFileRaw(ApiReportDroppedFileRaw(config['api_key'], config['server']), ACTION_REPORT_GET_DROPPED_FILE_RAW)),
            (ACTION_REPORT_GET_ENHANCED_SUMMARY, CliReportEnhancedSummary(ApiReportEnhancedSummary(config['api_key'], config['server']), ACTION_REPORT_GET_ENHANCED_SUMMARY)),
            (ACTION_REPORT_GET_FILE, CliReportFile(ApiReportFile(config['api_key'], config['server']), ACTION_REPORT_GET_FILE)),
            (ACTION_REPORT_GET_SCREENSHOTS, CliReportScreenshots(ApiReportScreenshots(config['api_key'], config['server']), ACTION_REPORT_GET_SCREENSHOTS)),
            (ACTION_REPORT_GET_SUMMARY, CliReportSummary(ApiReportSummary(config['api_key'], config['server']), ACTION_REPORT_GET_SUMMARY)),
            (ACTION_REPORT_GET_STATE, CliReportState(ApiReportState(config['api_key'], config['server']), ACTION_REPORT_GET_STATE)),

            (ACTION_SCAN_CONVERT_TO_FULL, CliScanConvertToFull(ApiScanConvertToFull(config['api_key'], config['server']), ACTION_SCAN_CONVERT_TO_FULL)),
            (ACTION_SCAN_FILE, CliScanFile(ApiScanFile(config['api_key'], config['server']), ACTION_SCAN_FILE)),
            (ACTION_SCAN_SCAN, CliScanScan(ApiScanScan(config['api_key'], config['server']), ACTION_SCAN_SCAN)),
            (ACTION_SCAN_STATE, CliScanState(ApiScanState(config['api_key'], config['server']), ACTION_SCAN_STATE)),
            (ACTION_SCAN_URL_FOR_ANALYSIS, CliScanUrlForAnalysis(ApiScanUrlForAnalysis(config['api_key'], config['server']), ACTION_SCAN_URL_FOR_ANALYSIS)),
            (ACTION_SCAN_URL_TO_FILE, CliScanUrlToFile(ApiScanUrlToFile(config['api_key'], config['server']), ACTION_SCAN_URL_TO_FILE)),

            (ACTION_SEARCH_HASH, CliSearchHash(ApiSearchHash(config['api_key'], config['server']), ACTION_SEARCH_HASH)),
            (ACTION_SEARCH_HASHES, CliSearchHashes(ApiSearchHashes(config['api_key'], config['server']), ACTION_SEARCH_HASHES)),
            (ACTION_SEARCH_STATES, CliSearchStates(ApiSearchStates(config['api_key'], config['server']), ACTION_SEARCH_STATES)),
            (ACTION_SEARCH_TERMS, CliSearchTerms(ApiSearchTerms(config['api_key'], config['server']), ACTION_SEARCH_TERMS)),

            (ACTION_SUBMIT_DROPPED_FILE, CliSubmitDroppedFile(ApiSubmitDroppedFile(config['api_key'], config['server']), ACTION_SUBMIT_DROPPED_FILE)),
            (ACTION_SUBMIT_FILE, CliSubmitFile(ApiSubmitFile(config['api_key'], config['server']), ACTION_SUBMIT_FILE)),
            (ACTION_SUBMIT_HASH_FOR_URL, CliSubmitHashForUrl(ApiSubmitHashForUrl(config['api_key'], config['server']), ACTION_SUBMIT_HASH_FOR_URL)),
            (ACTION_SUBMIT_REANALYZE, CliSubmitReanalyze(ApiSubmitReanalyze(config['api_key'], config['server']), ACTION_SUBMIT_REANALYZE)),
            (ACTION_SUBMIT_URL_FOR_ANALYSIS, CliSubmitUrlForAnalysis(ApiSubmitUrlForAnalysis(config['api_key'], config['server']), ACTION_SUBMIT_URL_FOR_ANALYSIS)),
            (ACTION_SUBMIT_URL_TO_FILE, CliSubmitUrlToFile(ApiSubmitUrlToFile(config['api_key'], config['server']), ACTION_SUBMIT_URL_TO_FILE)),

            (ACTION_SYSTEM_BACKEND, CliSystemBackend(ApiSystemBackend(config['api_key'], config['server']), ACTION_SYSTEM_BACKEND)),
            (ACTION_SYSTEM_ENVIRONMENTS, CliSystemEnvironments(ApiSystemEnvironments(config['api_key'], config['server']), ACTION_SYSTEM_ENVIRONMENTS)),
            (ACTION_SYSTEM_IN_PROGRESS, CliSystemInProgress(ApiSystemInProgress(config['api_key'], config['server']), ACTION_SYSTEM_IN_PROGRESS)),
            (ACTION_SYSTEM_HEARTBEAT, CliSystemHeartbeat(ApiSystemHeartbeat(config['api_key'], config['server']), ACTION_SYSTEM_HEARTBEAT)),
            (ACTION_SYSTEM_PHP, CliSystemPhp(ApiSystemPhp(config['api_key'], config['server']), ACTION_SYSTEM_PHP)),
            (ACTION_SYSTEM_STATE, CliSystemState(ApiSystemState(config['api_key'], config['server']), ACTION_SYSTEM_STATE)),
            (ACTION_SYSTEM_STATS, CliSystemStats(ApiSystemStats(config['api_key'], config['server']), ACTION_SYSTEM_STATS)),
            (ACTION_SYSTEM_QUEUE_SIZE, CliSystemQueueSize(ApiSystemQueueSize(config['api_key'], config['server']), ACTION_SYSTEM_QUEUE_SIZE)),
            (ACTION_SYSTEM_VERSION, CliSystemVersion(ApiSystemVersion(config['api_key'], config['server']), ACTION_SYSTEM_VERSION)),
        ])

    def check_current_key(self):
        config = self.config
        
        cli_object_key_current = CliKeyCurrent(ApiKeyCurrent(config['api_key'], config['server']), ACTION_KEY_CREATE)
        api_object_key_current = cli_object_key_current.api_object

        api_object_key_current.call(self.request_session, self.vxapi_cli_headers)
        api_key_data_json_response = api_object_key_current.get_response_json()

        if api_object_key_current.get_response_status_code() != 200 or bool(api_key_data_json_response) is False:
            base_error_message = 'Can\'t retrieve data for given API Key \'{}\' in the webservice: \'{}\'. Response status code: \'{}\''.format(config['api_key'], config['server'], api_object_key_current.get_response_status_code())
            if 'message' in api_key_data_json_response:
                base_error_message += '. Response message: \'{}\''.format(api_key_data_json_response['message'])

            raise RetrievingApiKeyDataError(base_error_message)
        
        return cli_object_key_current
    
    def prepare_parser(self, current_key_json, map_of_available_actions):
        parser = argparse.ArgumentParser(description=Color.control_without_arrows('{} [{}]'.format(self.program_name, self.program_version)), formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)
        parser.add_argument('--version', '-ver', action='version', version='{} - version {}'.format(self.program_name, self.program_version))
        DefaultCliArguments(parser).add_help_opt()

        subparsers = parser.add_subparsers(help='Action names for \'{}\' auth level'.format(current_key_json['auth_level_name']), dest="chosen_action")

        for name, value in map_of_available_actions.items():
            if isinstance(value, dict):
                child_parser = subparsers.add_parser(name=name, help=value['help_description'], add_help=False)
                value['parser_handler'](child_parser)
            elif value.api_object.endpoint_auth_level <= current_key_json['auth_level']:
                child_parser = subparsers.add_parser(name=name, help=value.help_description, add_help=False)
                value.add_parser_args(child_parser)

        
        return parser

    def prepare_args_iterations(self, args):
        args_iterations = []
        if args['chosen_action'] in ACTION_WITH_MULTIPLE_CALL_SUPPORT:
            for file in args['file']:
                arg_iter = args.copy()
                arg_iter['file'] = file
                args_iterations.append(arg_iter)
        else:
            args_iterations = [args]
            
        return args_iterations

    def prepare_api_query_usage_data(self, api_limits):
        api_usage = OrderedDict()
        api_usage_limits = api_limits['limits']
        is_api_limit_reached = False

        if api_limits['used']:
            for period, used_limit in api_limits['used'].items():
                # Given request is made after checking api limits. It means that we have to add 1 to current limits, to simulate that what happen after making requested API call
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
        current_key_cli_object = self.check_current_key()
        current_key_json = current_key_cli_object.api_object.get_response_json()
        current_key_response_headers = current_key_cli_object.api_object.get_headers()
        
        parser = self.prepare_parser(current_key_json, map_of_available_actions)
        args = self.rebuild_args(vars(parser.parse_args()))
        self.loaded_action = args['chosen_action']

        if self.loaded_action is not None:
            args_iterations = self.prepare_args_iterations(args)

            submission_limits = json.loads(current_key_response_headers['Submission-Limits']) if 'Submission-Limits' in current_key_response_headers else {}
            quick_scan_limits = json.loads(current_key_response_headers['Quick-Scan-Limits']) if 'Quick-Scan-Limits' in current_key_response_headers else {}
            api_limits = json.loads(current_key_response_headers['Api-Limits'])

            if_multiple_calls = True if args['chosen_action'] in ACTION_WITH_MULTIPLE_CALL_SUPPORT and len(args['file']) > 1 else False
            cli_object = map_of_available_actions[args['chosen_action']]

            if args['verbose'] is True:
                if isinstance(cli_object, dict) is False:
                    cli_object.init_verbose_mode()
                start_msg = 'Running \'{}\' in version \'{}\'. Webservice version: \'{}\', API version: \'{}\''.format(self.program_name, self.program_version, current_key_response_headers['Webservice-Version'], current_key_response_headers['Api-Version'])
                print(Color.control(start_msg))

            if self.loaded_action == ACTION_CHECK_LIMITS:
                if args['verbose'] is True:
                    if api_limits:
                        CliMsgPrinter.print_usage_info(api_limits['limits'], api_limits['used'], api_limits['limit_reached'])

                    CliMsgPrinter.print_submission_limit_info(submission_limits)
                    CliMsgPrinter.print_quick_scan_limit_info(quick_scan_limits)
                else:
                    print(Color.control('API query limits'))
                    print(api_limits)

                    print(Color.control('Submission limits'))
                    print(submission_limits)

                    print(Color.control('Quick scan submission limits'))
                    print(quick_scan_limits)

                print('\n')

                return

            CliPrompts.prompt_for_dir_content_submission(if_multiple_calls, args)
            CliPrompts.prompt_for_sharing_confirmation(args, self.config['server'])
            CliHelper.check_if_version_is_supported(args, current_key_response_headers['Webservice-Version'], self.config['server'])
            number_of_iterations = len(args_iterations)

            for index, arg_iter in enumerate(args_iterations):
                current_iteration = '{}/{}'.format(index + 1, number_of_iterations) if if_multiple_calls is True else None
                iter_cli_object = deepcopy(cli_object)
                iter_cli_object.attach_args(arg_iter)

                if api_limits and api_limits['limit_reached'] is True:
                    raise ReachedApiLimitError('Exceeded maximum API requests per {}({}). Please try again later.'.format(api_limits['name_of_reached_limit'], api_limits['used'][api_limits['name_of_reached_limit']]))

                if arg_iter['verbose'] is True:
                    # if arg_iter['chosen_action'] != ACTION_KEY_CURRENT and (if_multiple_calls is False or index == 0) and 'used' in api_limits:
                    if (if_multiple_calls is False or index == 0) and 'used' in api_limits:
                        CliMsgPrinter.print_usage_info(**self.prepare_api_query_usage_data(api_limits))

                    if if_multiple_calls is False or index == 0:
                        CliMsgPrinter.print_api_key_info(current_key_json)

                    if 'file' in arg_iter:
                        iter_cli_object.attach_file(arg_iter['file'])

                    if if_multiple_calls is False:
                        CliMsgPrinter.print_full_call_info(iter_cli_object)
                    else:
                        if index == 0:
                            CliMsgPrinter.print_shorten_call_info(iter_cli_object)

                        CliMsgPrinter.print_shortest_call_info(iter_cli_object, current_iteration)
                elif 'file' in arg_iter:
                    iter_cli_object.attach_file(arg_iter['file'])

                if arg_iter['chosen_action'] != ACTION_KEY_CURRENT:
                    try:
                        iter_cli_object.api_object.call(self.request_session, self.vxapi_cli_headers)
                    except Exception as e:
                        if if_multiple_calls is True:
                            CliMsgPrinter.print_error_info(e)
                        else:
                            raise e
                else:
                    iter_cli_object = current_key_cli_object

                if arg_iter['verbose'] is True:
                    CliMsgPrinter.print_response_summary(arg_iter, iter_cli_object, current_iteration)
                elif if_multiple_calls:
                    print(Color.control('{} - {}'.format(arg_iter['file'].name, current_iteration)))

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


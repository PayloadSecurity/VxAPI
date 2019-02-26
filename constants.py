import os
import sys

ACTION_SEARCH_HASH = 'search_hash'
ACTION_SEARCH_HASHES = 'search_hashes'
ACTION_SEARCH_STATES = 'search_states'
ACTION_SEARCH_TERMS = 'search_terms'

ACTION_OVERVIEW_GET = 'overview_get'
ACTION_OVERVIEW_REFRESH = 'overview_refresh'
ACTION_OVERVIEW_GET_SUMMARY = 'overview_get_summary'
ACTION_OVERVIEW_GET_SAMPLE = 'overview_download_sample'

ACTION_SUBMIT_DROPPED_FILE = 'submit_dropped_file'
ACTION_SUBMIT_FILE = 'submit_file'
ACTION_SUBMIT_HASH_FOR_URL = 'submit_hash_for_url'
ACTION_SUBMIT_REANALYZE = 'submit_reanalyze'
ACTION_SUBMIT_URL_FOR_ANALYSIS = 'submit_url_for_analysis'
ACTION_SUBMIT_URL_TO_FILE = 'submit_url_to_file'

ACTION_REPORT_GET_BULK_SUMMARY = 'report_get_bulk_summary'
ACTION_REPORT_GET_BULK_DEMO = 'report_get_demo_bulk'
ACTION_REPORT_GET_DROPPED_FILES = 'report_get_dropped_files'
ACTION_REPORT_GET_DROPPED_FILE_RAW = 'report_get_raw_dropped_file'
ACTION_REPORT_GET_ENHANCED_SUMMARY = 'report_get_enhanced_summary'
ACTION_REPORT_GET_FILE = 'report_get_file'
ACTION_REPORT_GET_SCREENSHOTS = 'report_get_screenshots'
ACTION_REPORT_GET_STATE = 'report_get_state'
ACTION_REPORT_GET_SUMMARY = 'report_get_summary'

ACTION_SYSTEM_VERSION = 'system_get_version'
ACTION_SYSTEM_ENVIRONMENTS = 'system_get_environments'
ACTION_SYSTEM_STATS = 'system_get_stats'
ACTION_SYSTEM_STATE = 'system_get_state'
ACTION_SYSTEM_PHP = 'system_get_php'
ACTION_SYSTEM_CONFIGURATION = 'system_get_configuration'
ACTION_SYSTEM_BACKEND = 'system_get_backend'
ACTION_SYSTEM_QUEUE_SIZE = 'system_get_queue_size'
ACTION_SYSTEM_IN_PROGRESS = 'system_get_in_progress_stats'
ACTION_SYSTEM_TOTAL_SUBMISSION = 'system_get_total_submissions_stats'
ACTION_SYSTEM_HEARTBEAT = 'system_get_heartbeat'

ACTION_KEY_CURRENT = 'key_get_current'
ACTION_KEY_CREATE = 'key_create'

ACTION_FEED = 'feed_get'
ACTION_FEED_LATEST = 'feed_get_latest'

ACTION_SCAN_CONVERT_TO_FULL = 'scan_convert_to_full'
ACTION_SCAN_FILE = 'scan_file'
ACTION_SCAN_SCAN = 'scan_get_result'
ACTION_SCAN_STATE = 'scan_get_scanners'
ACTION_SCAN_URL_FOR_ANALYSIS = 'scan_url_for_analysis'
ACTION_SCAN_URL_TO_FILE = 'scan_url_to_file'

MINIMAL_SUPPORTED_INSTANCE_VERSION = '8.2'
CLI_BASE_PATH = os.path.dirname(os.path.realpath(__file__))
CALLED_SCRIPT = sys.argv[0]

ACTION_WITH_MULTIPLE_CALL_SUPPORT = [ACTION_SUBMIT_FILE, ACTION_SCAN_FILE]

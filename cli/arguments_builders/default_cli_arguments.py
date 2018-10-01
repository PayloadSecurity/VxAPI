import argparse
from argparse import ArgumentParser
from constants import ACTION_GET_ENVIRONMENTS


class DefaultCliArguments:

    def __init__(self, parser: ArgumentParser):
        self.parser = parser

    def add_sha256_arg(self, help='Sample sha256 hash'):
        self.parser.add_argument('sha256', type=str, help=help)

    def add_hash_arg(self, help='Md5, sha1 or sha256 hash'):
        self.parser.add_argument('hash', type=str, help=help)

    def add_env_id_arg(self):
        self.parser.add_argument('env-id', type=int, help='Environment Id')

    def add_id_arg(self):
        self.parser.add_argument('id', type=str, help='Id in one of format: \'jobId\' or \'sha256:environmentId\'')

    def add_feed_days_arg(self):
        self.parser.add_argument('days', type=int, help='Number of days')

    def add_key_uid_arg(self):
        self.parser.add_argument('uid', type=str, help='Any string to allow find this key later')

    def add_datetime_from_arg(self): # TODO - add datetime validator
        self.parser.add_argument('date-from', type=str, help='From date. Please specify in the following format: ‘Y-m-d H:i:s’')

    def add_datetime_to_arg(self):
        self.parser.add_argument('date-to', type=str, help='To date. Please specify in the following format: ‘Y-m-d H:i:s’')

    def add_nssf_format_output_opt(self):
        self.parser.add_argument('--format', '-f', type=str, help='Output format', choices=['md5', 'sha1', 'sha256'], default='sha256')

    def add_nssf_visibility_opt(self):
        self.parser.add_argument('--visibility', '-vs', type=str, help='Output format', choices=['all', 'public', 'private'], default='public')

    def add_nssf_type_opt(self):
        self.parser.add_argument('--type', '-t', type=str, help='Type of samples', choices=['all', 'malicious', 'clean'], default='all')

    def add_file_output_path_opt(self):
        self.parser.add_argument('--output', '-o', type=str, default='output', help='File output path')

    def add_submit_name_option(self):
        self.parser.add_argument('--submitname', '-sn', type=str, help='\'submission name\' field that will be used for file type detection and analysis')

    def add_comment_argument(self):
        self.parser.add_argument('--comment', '-c', type=str, help='Add comment (e.g. #hashtag) to sample')

    def add_file_with_hash_list_arg(self, allowed_hashes):
        self.parser.add_argument('hashes-file', type=argparse.FileType('r'), help='Path to file containing list of sample hashes separated by new line (allowed: {})'.format(', '.join(allowed_hashes)))

    def add_file_with_ids_arg(self, allowed_ids):
        self.parser.add_argument('mixed-ids-file', type=argparse.FileType('r'), help='Path to file containing list of ids (allowed: {}'.format(', '.join(allowed_ids)))

    def add_report_file_type_arg(self):
        self.parser.add_argument('type', type=str, choices=['bin', 'json', 'pdf', 'crt', 'maec', 'stix', 'misp', 'misp-json', 'openioc', 'html', 'pcap', 'memory', 'xml'], help='Type of requested content')

    def add_report_demo_bulk_modify_hash_opt(self):
        self.parser.add_argument('--modify-hash', '-mh', action='store_true', default=False, help='When set, will add null byte at the end of sample file')

    def add_report_demo_bulk_av_min_opt(self):
        self.parser.add_argument('--av-min', '-an', type=int, default=5, help='The minimum required AV detect')

    def add_report_demo_bulk_av_max_opt(self):
        self.parser.add_argument('--av-max', '-ax', type=int, default=15, help='The maximum required AV detect')

    def add_report_demo_bulk_look_back_size_opt(self):
        self.parser.add_argument('--look-back-size', '-lbs', type=int, default=400, help='Number of samples which will be fetched and filtered. Once you will get error message about problem with finding all samples, please increase that value')

    def add_submission_file(self):
        self.parser.add_argument('file', type=argparse.FileType('rb'), help='File to submit')

    def add_submission_no_share_third_party_opt(self):
        self.parser.add_argument('--private', '-pv', help='When set to \'1\', the sample is never shared with any third party', type=int, choices=['1', '0'], default='1')

    def add_submission_allow_community_access_opt(self):
        self.parser.add_argument('--allow-community-access', '-aca', choices=['1', '0'], default='1', type=int, help='When set \'1\', the sample will be available for vetted users of the HA community or custom application server')

    def add_submission_no_hash_lookup(self):
        self.parser.add_argument('--no-hash-lookup', '-nhl', choices=['1', '0'], default='1', type=int)

    def add_submission_action_script_opt(self):
        self.parser.add_argument('--action-script', '-ac', choices={1: 'default', 2: 'default_maxantievasion', 3: 'default_randomfiles', 4: 'default_randomtheme', 5: 'default_openie'}, default=1, type=int, help='Optional custom runtime action script')

    def add_submission_hybrid_analysis_opt(self):
        self.parser.add_argument('--hybrid-analysis', '-ha', choices=['1', '0'], default='1', type=str, help='When set to \'0\', no memory dumps or memory dump analysis will take placd')

    def add_submission_experimental_anti_evasion_opt(self):
        self.parser.add_argument('--experimental-anti_evasion', '-eae', choices=['1', '0'], default='0', type=str, help='When set to \'1\', will set all experimental anti-evasion options of the Kernelmode Monitor')

    def add_submission_script_logging_opt(self):
        self.parser.add_argument('--script-logging', '-sl', choices=['1', '0'], default='1', type=str, help='When set to \'1\', will set the in-depth script logging engine of the Kernelmode Monitor')

    def add_submission_input_sample_tampering_opt(self):
        self.parser.add_argument('--allow-community-access', '-aca', choices=['1', '0'], default='0', type=str, help='When set to \'1\', will allow experimental anti-evasion options of the Kernelmode Monitor that tamper with the input sample')

    def add_submission_tor_enabled_analysis_opt(self):
        self.parser.add_argument('--tor-enabled-analysis', '-tea', choices=['1', '0'], default='0', type=str, help='When set to \'1\', will route the network traffic for the analysis via TOR (if properly configured on the server)')

    def add_submission_offline_analysis_opt(self):
        self.parser.add_argument('--offline-analysis', '-oa', choices=['1', '0'], default='0', type=str, help='When set to \'1\', will disable outbound network traffic for the guest VM (takes precedence over ‘tor-enabled-analysis’ if both are provided)')

    def add_submission_email_opt(self): # TODO - kontynuuj dla submit file
        self.parser.add_argument('--email', '-e', type=str, help='Optional E-Mail address that may be associated with the submission for notification')

    def add_submission_input_sample_tampering_opt(self):
        self.parser.add_argument('--allow-community-access', '-aca', choices=['1', '0'], default='1', type=str, help='')

    def add_submission_input_sample_tampering_opt(self):
        self.parser.add_argument('--allow-community-access', '-aca', choices=['1', '0'], default='1', type=str, help='')

    def add_submission_input_sample_tampering_opt(self):
        self.parser.add_argument('--allow-community-access', '-aca', choices=['1', '0'], default='1', type=str, help='')

    def add_priority_argument(self):
        def check_value_range(value):
            forced_int_value = int(value)
            if forced_int_value < 0 or forced_int_value > 100:
                raise argparse.ArgumentTypeError('{} is not a value between 0 and 100'.format(value))
            return forced_int_value

        self.parser.add_argument('--priority', '-pr', type=check_value_range, help='Priority value between 0 (default) and 100 (highest)')

    def add_hash_argument(self):
        self.parser.add_argument('hash', type=str, help='Sample hash (md5, sha1 or sha256)')

    def add_dropped_file_name_argument(self):
        self.parser.add_argument('fileName', type=str, help='Dropped file name')

    def add_environment_id_argument(self, required: bool = False):
        environment_id_help = 'Sample Environment ID (use \'{}\' action to fetch all available)'.format(ACTION_GET_ENVIRONMENTS)
        if required is False:
            self.parser.add_argument('--environmentId', '-env', type=int, help=environment_id_help)
        else:
            self.parser.add_argument('environmentId', type=int, help=environment_id_help)

    def add_nosharevt_argument(self):
        self.parser.add_argument('--private', '-pv', help='When set to \'1\', the sample is never shared with any third party', type=str, choices=['1', '0'], default='1', dest="nosharevt")

    def add_days_argument(self):
        self.parser.add_argument('days', type=str, help='Days')

    def add_report_file_type(self):
        self.parser.add_argument('--type', '-t', type=str, choices=['bin', 'json', 'pdf', 'crt', 'maec', 'misp', 'misp-json', 'openioc', 'html', 'pcap', 'memory', 'xml'], help='File type to return')

    def add_cli_output_argument(self):
        self.parser.add_argument('--cli_output', '-o', type=str, default='output', help='Output path')

    def add_query_search_argument(self):
        self.parser.add_argument('query', type=str, help='Search query. Once you want to search by multiple terms, wrap it into quotes e.g. \'python3 vxapi.py search "filetype_tag:doc filename:invoice"\'')

    def add_submit_file_argument(self):
        self.parser.add_argument('file', type=argparse.FileType('rb'), help='File to submit')

    def add_submitted_document_password_argument(self):
        self.parser.add_argument('--document-password', '-dp', type=str, help='Password used for archive extraction', dest="documentPassword")

    def add_analyze_url_argument(self):
        self.parser.add_argument('analyzeurl', type=str, help='Url which contains file')

    def add_url_file_argument(self):
        self.parser.add_argument('fileurl', type=str, help='Url which contains file')

    def add_url_hash_argument(self):
        self.parser.add_argument('url', type=str, help='Url to hash')

    def add_verbose_argument(self):
        self.parser.add_argument('--verbose', '-v', help="Run command in verbose mode", action='store_true')

    def add_help_argument(self):
        self.parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')

    def add_quiet_argument(self):
        self.parser.add_argument('--quiet', '-q', action='store_true', default=False, help='Suppress all prompts and warnings')

    def add_hash_format_argument(self):
        self.parser.add_argument('--hash-format', '-hf', choices=['md5', 'sha1', 'sha256', 'sha256'], default='md5', help='Type of returned hash', dest="format")

    def add_visibility_argument(self):
        self.parser.add_argument('--visibility', '-vs', choices=['all', 'private', 'public'], default='public', help='Samples visibility')

    def add_verdict_format_argument(self):
        self.parser.add_argument('--verdict-format', '-vf', choices=['all', 'malicious', 'clean'], default='all', help='Samples verdict format', dest="type")

    def add_from_date_argument(self):
        self.parser.add_argument('from', type=str, help='Filter from date - ISO format')

    def add_to_date_argument(self):
        self.parser.add_argument('to', type=str, help='Filter to date - ISO format')

    def add_file_with_hash_list_with_envs(self):
        self.parser.add_argument('hash_list_with_envs', type=argparse.FileType('r'), help='Path to file containing list of sample hashes with environment IDs (hash:envId)')

    def add_allow_community_access_param(self):
        self.parser.add_argument('--allow_community_access', '-aca', choices=['1', '0'], default='1', type=str, help='When set \'1\', the sample will be available for vetted users of the HA community or custom application server', dest='allowCommunityAccess')


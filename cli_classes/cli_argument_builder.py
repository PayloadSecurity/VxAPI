import argparse
from argparse import ArgumentParser
from constants import ACTION_GET_ENVIRONMENTS


class CliArgumentBuilder:

    def __init__(self, parser: ArgumentParser):
        self.parser = parser

    def add_sha256_argument(self):
        self.parser.add_argument('sha256', type=str, help='Sample sha256 hash')

    def add_submit_name_argument(self):
        self.parser.add_argument('--submitname', '-sn', type=str, help='\'submission name\' field that will be used for file type detection and analysis')

    def add_comment_argument(self):
        self.parser.add_argument('--comment', '-c', type=str, help='Add comment (e.g. #hashtag) to sample')

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
        pass
        # self.parser.add_argument('--nosharevt', '-n', help='Do not share with community', action='store_false') - temporary disabled due to unclear logic on webservice

    def add_days_argument(self):
        self.parser.add_argument('days', type=str, help='Days')

    def add_file_type_argument(self):
        self.parser.add_argument('--type', '-t', type=str, choices=['bin', 'json', 'pdf', 'crt', 'maec', 'misp', 'openioc', 'html', 'pcap', 'memory', 'xml'], default='xml', help='File type to return')

    def add_public_file_type_argument(self):
        self.parser.add_argument('--type', '-t', type=str, choices=['bin', 'pcap'], default='bin', help='File type to return')

    def add_cli_output_argument(self):
        self.parser.add_argument('--cli_output', '-o', type=str, default='output', help='Output path')

    def add_query_search_argument(self):
        self.parser.add_argument('query', type=str, help='Search query')

    def add_submit_file_argument(self):
        self.parser.add_argument('file', type=argparse.FileType('rb'), help='File to submit')

    def add_analyze_url_argument(self):
        self.parser.add_argument('analyzeurl', type=str, help='Url which contains file')

    def add_url_file_argument(self):
        self.parser.add_argument('fileurl', type=str, help='Url which contains file')

    def add_verbose_argument(self):
        self.parser.add_argument('--verbose', '-v', help="Run command in verbose mode", action='store_true')

    def add_help_argument(self):
        self.parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')

import argparse
from argparse import ArgumentParser
from constants import ACTION_SYSTEM_ENVIRONMENTS
from constants import ACTION_SCAN_STATE
import os


class DefaultCliArguments:

    def __init__(self, parser: ArgumentParser):
        self.parser = parser

    def add_sha256_arg(self, help='Sample sha256 hash'):
        self.parser.add_argument('sha256', type=str, help=help)

        return self

    def add_hash_arg(self, help='Md5, sha1 or sha256 hash'):
        self.parser.add_argument('hash', type=str, help=help)

        return self

    def add_scan_type_arg(self):
        self.parser.add_argument('scan-type', type=str, help='Type of scan (please use \'{}\' action to fetch all available scanners)'.format(ACTION_SCAN_STATE))

        return self

    def add_url_arg(self, help):
        self.parser.add_argument('url', type=str, help=help)

        return self

    def add_id_arg(self, help='Id in one of format: \'jobId\' or \'sha256:environmentId\''):
        self.parser.add_argument('id', type=str, help=help)

        return self

    def add_feed_days_arg(self):
        self.parser.add_argument('days', type=int, help='Number of days')

        return self

    def add_key_uid_arg(self):
        self.parser.add_argument('uid', type=str, help='Any string to allow find this key later')

        return self

    def add_file_with_hash_list_arg(self, allowed_hashes):
        self.parser.add_argument('hashes-file', type=argparse.FileType('r'), help='Path to file containing list of sample hashes separated by new line (allowed: {})'.format(', '.join(allowed_hashes)))

        return self

    def add_file_with_ids_arg(self, allowed_ids):
        self.parser.add_argument('mixed-ids-file', type=argparse.FileType('r'), help='Path to file containing list of ids (allowed: {}'.format(', '.join(allowed_ids)))

        return self

    def add_report_file_type_opt_arg(self):
        self.parser.add_argument('type', type=str, choices=['bin', 'json', 'pdf', 'crt', 'maec', 'stix', 'misp', 'misp-json', 'openioc', 'html', 'pcap', 'memory', 'xml'], help='Type of requested content')

        return self

    def add_submit_files_arg(self):
        def validate_path(path):
            files = [path]
            if os.path.exists(path) is False:
                raise argparse.ArgumentTypeError('No such file or directory: \'{}\''.format(path))

            if os.path.isdir(path):
                if path.startswith('/') is True:  # Given path is absolute
                    abs_path = path
                else:
                    abs_path = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-2] + [path])

                files = list(filter(lambda path: os.path.isfile(path), ['{}/{}'.format(abs_path, x) for x in os.listdir(path)]))

            return files

        self.parser.add_argument('file', type=validate_path, help='File to submit (when directory given, all files from it will be submitted - non recursively)')

        return self

    def add_file_output_path_opt(self):
        self.parser.add_argument('--output', '-o', type=str, default='output', help='File output path')

    def add_env_id_arg(self, required: bool = False):
        environment_id_help = 'Sample Environment ID (use \'{}\' action to fetch all available)'.format(ACTION_SYSTEM_ENVIRONMENTS)
        if required is False:
            self.parser.add_argument('--environment-id', '-env', type=int, help=environment_id_help)
        else:
            self.parser.add_argument('environment-id', type=int, help=environment_id_help)

        return self

    def add_report_file_type_opt(self):
        self.parser.add_argument('--type', '-t', type=str, choices=['bin', 'json', 'pdf', 'crt', 'maec', 'misp', 'misp-json', 'openioc', 'html', 'pcap', 'memory', 'xml'], help='File type to return')

        return self

    def add_verbose_arg(self):
        self.parser.add_argument('--verbose', '-v', help="Run command in verbose mode", action='store_true')

        return self

    def add_help_opt(self):
        self.parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')

        return self

    def add_quiet_opt(self):
        self.parser.add_argument('--quiet', '-q', action='store_true', default=False, help='Suppress all prompts and warnings')

        return self



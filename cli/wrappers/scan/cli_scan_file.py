from cli.wrappers.cli_caller import CliCaller
from constants import ACTION_OVERVIEW_GET


class CliScanFile(CliCaller):

    help_description = 'Submit a file for quick scan (you can check results by \'' + ACTION_OVERVIEW_GET + '\' action) by \'{}\''

    def add_parser_args(self, child_parser): # TODO -add the rest of parameters
        parser_argument_builder = super(CliScanFile, self).add_parser_args(child_parser)
        parser_argument_builder.add_submit_files_arg()
        parser_argument_builder.add_scan_type_arg()


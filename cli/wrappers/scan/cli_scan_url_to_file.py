from cli.wrappers.cli_caller import CliCaller
from constants import ACTION_OVERVIEW_GET


class CliScanUrlToFile(CliCaller):

    help_description = 'Submit a file by url for quick scan (you can check results by \'' + ACTION_OVERVIEW_GET + '\' action) by \'{}\''

    def add_parser_args(self, child_parser): # TODO -add the rest of parameters
        parser_argument_builder = super(CliScanUrlToFile, self).add_parser_args(child_parser)
        parser_argument_builder.add_url_arg('Url of file to submit')
        parser_argument_builder.add_scan_type_arg()

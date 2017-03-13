from cli_classes.cli_caller import CliCaller
from cli_classes.cli_argument_builder import CliArgumentBuilder


class CliScan(CliCaller):

    help_description = 'Get scan of the file by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliScan, self).add_parser_args(child_parser)
        parser_argument_builder.add_sha256_argument()

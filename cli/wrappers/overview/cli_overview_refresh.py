from cli.wrappers.cli_caller import CliCaller


class CliOverviewRefresh(CliCaller):

    help_description = 'Refresh overview and download fresh data from external services by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliOverviewRefresh, self).add_parser_args(child_parser)
        parser_argument_builder.add_sha256_arg()

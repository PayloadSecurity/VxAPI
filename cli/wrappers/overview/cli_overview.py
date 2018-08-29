from cli.wrappers.cli_caller import CliCaller


class CliOverview(CliCaller):

    help_description = 'Return overview for hash by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliOverview, self).add_parser_args(child_parser)
        parser_argument_builder.add_sha256_arg()



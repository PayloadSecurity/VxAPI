from cli.wrappers.cli_caller import CliCaller


class CliSummary(CliCaller):

    help_description = 'Get an analysis of the summary by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliSummary, self).add_parser_args(child_parser)
        parser_argument_builder.add_hash_argument()
        parser_argument_builder.add_environment_id_argument(True)

from cli.wrappers.cli_caller import CliCaller


class CliReportEnhancedSummary(CliCaller):

    help_description = 'Return enhanced summary of a submission by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliReportEnhancedSummary, self).add_parser_args(child_parser)
        parser_argument_builder.add_id_arg()


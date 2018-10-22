from cli.wrappers.cli_caller import CliCaller


class CliReportSummary(CliCaller):

    help_description = 'Return summary of a submission by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliReportSummary, self).add_parser_args(child_parser)
        parser_argument_builder.add_id_arg()


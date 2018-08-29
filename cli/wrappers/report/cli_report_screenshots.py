from cli.wrappers.cli_caller import CliCaller


class CliReportScreenshots(CliCaller):

    help_description = 'Retrieve an array of screenshots from a report in the Base64 format by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliReportScreenshots, self).add_parser_args(child_parser)
        parser_argument_builder.add_id_arg()

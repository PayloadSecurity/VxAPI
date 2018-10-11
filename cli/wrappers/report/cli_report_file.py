from cli.wrappers.cli_caller import CliCaller


class CliReportFile(CliCaller):

    help_description = 'Download report data (e.g. JSON, XML, PCAP) by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliReportFile, self).add_parser_args(child_parser)
        parser_argument_builder.add_id_arg()
        parser_argument_builder.add_report_file_type_opt_arg()
        parser_argument_builder.add_file_output_path_opt()

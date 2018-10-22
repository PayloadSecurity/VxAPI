from cli.wrappers.cli_caller import CliCaller


class CliReportDroppedFiles(CliCaller):

    help_description = 'Retrieve all extracted/dropped binaries files for a report as zip by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliReportDroppedFiles, self).add_parser_args(child_parser)
        parser_argument_builder.add_id_arg()
        parser_argument_builder.add_file_output_path_opt()

from cli.wrappers.cli_caller import CliCaller


class CliReportDroppedFileRaw(CliCaller):

    help_description = 'Retrieve single extracted/dropped binaries files for a report by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliReportDroppedFileRaw, self).add_parser_args(child_parser)
        parser_argument_builder.add_id_arg()
        parser_argument_builder.add_hash_arg('SHA256 of dropped file')
        parser_argument_builder.add_file_output_path_opt()

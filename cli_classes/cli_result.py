from cli.wrappers.cli_file_saver import CliFileSaver


class CliResult(CliFileSaver):

    help_description = 'Get report data by  \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliResult, self).add_parser_args(child_parser)
        parser_argument_builder.add_sha256_argument()
        parser_argument_builder.add_environment_id_argument()
        parser_argument_builder.add_file_type_argument()
        parser_argument_builder.add_cli_output_argument()


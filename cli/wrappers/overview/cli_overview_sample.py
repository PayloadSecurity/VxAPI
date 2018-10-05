from cli.wrappers.cli_caller import CliCaller


class CliOverviewSample(CliCaller):

    help_description = 'Downloading sample file by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliOverviewSample, self).add_parser_args(child_parser)
        parser_argument_builder.add_sha256_arg()
        parser_argument_builder.add_file_output_path_opt()



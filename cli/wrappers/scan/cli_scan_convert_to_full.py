from cli.wrappers.cli_caller import CliCaller


class CliScanConvertToFull(CliCaller):

    help_description = 'Convert quick scan to sandbox report by \'{}\''

    def add_parser_args(self, child_parser): # TODO -add the rest of parameters
        parser_argument_builder = super(CliScanConvertToFull, self).add_parser_args(child_parser)
        parser_argument_builder.add_id_arg()
        parser_argument_builder.add_environment_id_argument(True)

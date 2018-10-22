from cli.wrappers.cli_caller import CliCaller


class CliScanScan(CliCaller):

    help_description = 'Get quick scan results (worth to use when submission endpoint didn\'t return full data) by  \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliScanScan, self).add_parser_args(child_parser)
        parser_argument_builder.add_id_arg('ID of scan')

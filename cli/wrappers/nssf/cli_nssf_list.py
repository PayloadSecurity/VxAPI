from cli.wrappers.cli_caller import CliCaller


class CliNssfList(CliCaller):

    help_description = 'Return list of hashes for a given date range, verdict and published status by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliNssfList, self).add_parser_args(child_parser)
        parser_argument_builder.add_datetime_from_arg()
        parser_argument_builder.add_datetime_to_arg()
        parser_argument_builder.add_nssf_format_output_opt()
        parser_argument_builder.add_nssf_visibility_opt()
        parser_argument_builder.add_nssf_type_opt()

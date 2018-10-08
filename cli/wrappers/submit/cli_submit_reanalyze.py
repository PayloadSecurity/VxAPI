from cli.wrappers.cli_caller import CliCaller


class CliSubmitReanalyze(CliCaller):

    help_description = 'Reanalyze a generated report by \'{}\''

    def add_parser_args(self, child_parser): # TODO - add missing parameters
        parser_argument_builder = super(CliSubmitReanalyze, self).add_parser_args(child_parser)
        parser_argument_builder.add_id_arg()
        parser_argument_builder.add_no_share_third_party_opt()


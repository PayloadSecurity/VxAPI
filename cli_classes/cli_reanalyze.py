from cli.wrappers.cli_caller import CliCaller


# hash, 'environmentId', 'nosharevt', 'nohashlookup', 'kernelmode'
class CliReanalyze(CliCaller):

    help_description = 'Reanalyze sample by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliReanalyze, self).add_parser_args(child_parser)
        parser_argument_builder.add_sha256_argument()
        parser_argument_builder.add_environment_id_argument()
        parser_argument_builder.add_no_share_third_party_opt()
        # TODO - think about which of available flags should be available by CLI. Also check if the send parameters by API are working well on the webservice

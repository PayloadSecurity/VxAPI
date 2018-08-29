from cli.wrappers.cli_caller import CliCaller


class CliUrlHash(CliCaller):

    help_description = 'Get sha256 hash from url by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliUrlHash, self).add_parser_args(child_parser)
        parser_argument_builder.add_url_hash_argument()

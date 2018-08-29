from cli.wrappers.cli_caller import CliCaller


class CliSearchHash(CliCaller):

    help_description = 'Get summary for given hash by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliSearchHash, self).add_parser_args(child_parser)
        parser_argument_builder.add_hash_arg()

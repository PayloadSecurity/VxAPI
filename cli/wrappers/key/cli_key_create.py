from cli.wrappers.cli_caller import CliCaller


class CliKeyCreate(CliCaller):

    help_description = 'Create new API key with restricted auth level by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliKeyCreate, self).add_parser_args(child_parser)
        parser_argument_builder.add_key_uid_arg()

from cli.wrappers.cli_caller import CliCaller


class CliSearchStates(CliCaller):

    help_description = 'Get states for given ids by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliSearchStates, self).add_parser_args(child_parser)
        parser_argument_builder.add_file_with_ids_arg(['jobId', 'md5:environmentId'])

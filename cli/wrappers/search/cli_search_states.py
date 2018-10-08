from cli.wrappers.cli_caller import CliCaller


class CliSearchStates(CliCaller):

    help_description = 'Get states for given ids by \'{}\''

    def attach_args(self, args):
        super(CliSearchStates, self).attach_args(self.convert_file_hashes_to_array(args, 'mixed_ids_file', 'ids'))

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliSearchStates, self).add_parser_args(child_parser)
        parser_argument_builder.add_file_with_ids_arg(['jobId', 'sha256:environmentId'])

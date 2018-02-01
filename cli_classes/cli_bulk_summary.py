from cli_classes.cli_caller import CliCaller


class CliBulkSummary(CliCaller):

    help_description = 'Get bulk summary of the file by \'{}\''

    def attach_args(self, args):
        super(CliBulkSummary, self).attach_args(self.convert_file_hashes_to_array(args, 'hash_list_with_envs'))

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliBulkSummary, self).add_parser_args(child_parser)
        parser_argument_builder.add_file_with_hash_list_with_envs()

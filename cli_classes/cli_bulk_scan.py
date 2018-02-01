from cli_classes.cli_caller import CliCaller


class CliBulkScan(CliCaller):

    help_description = 'Get bulk scan of the file by \'{}\''

    def attach_args(self, args):
        super(CliBulkScan, self).attach_args(self.convert_file_hashes_to_array(args))

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliBulkScan, self).add_parser_args(child_parser)
        parser_argument_builder.add_file_with_hash_list()

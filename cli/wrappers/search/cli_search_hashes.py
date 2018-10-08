from cli.wrappers.cli_caller import CliCaller


class CliSearchHashes(CliCaller):

    help_description = 'Get summary for given hashes by \'{}\''

    def attach_args(self, args):
        super(CliSearchHashes, self).attach_args(self.convert_file_hashes_to_array(args, 'hashes_file'))

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliSearchHashes, self).add_parser_args(child_parser)
        parser_argument_builder.add_file_with_hash_list_arg(['md5', 'sha1', 'sha256'])

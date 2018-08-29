from cli.wrappers.cli_caller import CliCaller


class CliNssfDownload(CliCaller):

    help_description = 'Return an archive with a collection of samples by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliNssfDownload, self).add_parser_args(child_parser)
        parser_argument_builder.add_file_with_hash_list_arg(['md5', 'sha1', 'sha256', 'sha512'])
        parser_argument_builder.add_file_output_path_opt()

    def attach_args(self, args):
        super(CliNssfDownload, self).attach_args(self.convert_file_hashes_to_array(args))

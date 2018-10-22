from cli.wrappers.cli_caller import CliCaller


class CliReportBulkSummary(CliCaller):

    help_description = 'Return summary of multiple submissions (bulk query) by \'{}\''

    def attach_args(self, args):
        super(CliReportBulkSummary, self).attach_args(self.convert_file_hashes_to_array(args, 'mixed_ids_file'))

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliReportBulkSummary, self).add_parser_args(child_parser)
        parser_argument_builder.add_file_with_ids_arg(['jobId', 'md5:environmentId', 'sha1:environmentId', 'sha256:environmentId'])


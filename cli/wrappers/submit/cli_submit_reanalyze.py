from cli.wrappers.cli_caller import CliCaller
from cli.arguments_builders.submission_cli_arguments import SubmissionCliArguments


class CliSubmitReanalyze(CliCaller):

    help_description = 'Reanalyze a generated report by \'{}\''

    def build_argument_builder(self, child_parser):
        return SubmissionCliArguments(child_parser)

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliSubmitReanalyze, self).add_parser_args(child_parser)
        parser_argument_builder.add_id_arg()
        parser_argument_builder.add_submission_no_share_third_party_opt()
        parser_argument_builder.add_submission_no_hash_lookup()


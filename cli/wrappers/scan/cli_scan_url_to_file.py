from cli.wrappers.cli_caller import CliCaller
from constants import ACTION_OVERVIEW_GET
from cli.arguments_builders.submission_cli_arguments import SubmissionCliArguments


class CliScanUrlToFile(CliCaller):

    help_description = 'Submit a file by url for quick scan (you can check results by \'' + ACTION_OVERVIEW_GET + '\' action) by \'{}\''

    def build_argument_builder(self, child_parser):
        return SubmissionCliArguments(child_parser)

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliScanUrlToFile, self).add_parser_args(child_parser)
        parser_argument_builder.add_url_arg('Url of file to submit')
        parser_argument_builder.add_scan_type_arg()
        parser_argument_builder.add_submission_no_share_third_party_opt()
        parser_argument_builder.add_submission_allow_community_access_opt()
        parser_argument_builder.add_submission_comment_opt()
        parser_argument_builder.add_submission_submit_name_opt()

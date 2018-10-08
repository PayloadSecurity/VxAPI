from cli.wrappers.cli_caller import CliCaller


class CliSubmitFile(CliCaller):
    help_description = 'Submit file by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliSubmitFile, self).add_parser_args(child_parser)
        parser_argument_builder.add_submit_file_argument()
        parser_argument_builder.add_environment_id_argument()
        parser_argument_builder.add_submitted_document_password_argument()
        parser_argument_builder.add_no_share_third_party_opt()
        parser_argument_builder.add_allow_community_access_param()
        parser_argument_builder.add_submit_name_option()
        parser_argument_builder.add_comment_argument()
        parser_argument_builder.add_priority_argument()
        # TODO - think about which of available flags should be available by CLI.

from cli.wrappers.cli_caller import CliCaller
from cli.arguments_builders.submission_cli_arguments import SubmissionCliArguments


class CliSubmitUrlToFile(CliCaller):

    help_description = 'Submit a file by url for analysis by \'{}\''

    def build_argument_builder(self, child_parser):
        return SubmissionCliArguments(child_parser)

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliSubmitUrlToFile, self).add_parser_args(child_parser)
        parser_argument_builder.add_url_arg('Url for analyze')
        parser_argument_builder.add_env_id_arg(True)
        parser_argument_builder.add_submission_no_share_third_party_opt()
        parser_argument_builder.add_submission_allow_community_access_opt()
        parser_argument_builder.add_submission_no_hash_lookup()
        parser_argument_builder.add_submission_action_script_opt()
        parser_argument_builder.add_submission_hybrid_analysis_opt()
        parser_argument_builder.add_submission_experimental_anti_evasion_opt()
        parser_argument_builder.add_submission_script_logging_opt()
        parser_argument_builder.add_submission_input_sample_tampering_opt()
        parser_argument_builder.add_submission_tor_enabled_analysis_opt()
        parser_argument_builder.add_submission_offline_analysis_opt()
        parser_argument_builder.add_submission_email_opt()
        parser_argument_builder.add_submission_comment_opt()
        parser_argument_builder.add_submission_custom_date_time_opt()
        parser_argument_builder.add_submission_custom_cmd_line_opt()
        parser_argument_builder.add_submission_custom_run_time_opt()
        parser_argument_builder.add_submission_client_opt()
        parser_argument_builder.add_submission_submit_name_opt()
        parser_argument_builder.add_submission_priority_opt()
        parser_argument_builder.add_submission_document_password_opt()
        parser_argument_builder.add_submission_environment_variable_opt()

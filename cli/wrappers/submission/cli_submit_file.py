from cli.wrappers.cli_caller import CliCaller


class CliSubmitFile(CliCaller):

    help_description = 'Submit a file for analysis by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliSubmitFile, self).add_parser_args(child_parser)
        parser_argument_builder.add_submission_file()
        parser_argument_builder.add_env_id_arg()
        parser_argument_builder.add_submission_no_share_third_party_opt()

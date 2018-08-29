from cli.wrappers.cli_caller import CliCaller


class CliSampleDroppedFiles(CliCaller):

    help_description = 'Get dropped files by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliSampleDroppedFiles, self).add_parser_args(child_parser)
        parser_argument_builder.add_sha256_argument()
        parser_argument_builder.add_environment_id_argument()
        parser_argument_builder.add_cli_output_argument()

    def save_files(self):
        api_response = self.api_object.api_response
        f_out_name = self.cli_output_folder + '/VxStream_dropped_files_{}.zip'.format(self.given_args['sha256'])

        f_out = open(f_out_name, 'wb')
        f_out.write(api_response.content)
        f_out.close()

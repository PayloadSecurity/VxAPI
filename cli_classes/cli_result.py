from cli_classes.cli_caller import CliCaller
from io import BytesIO
import gzip


class CliResult(CliCaller):

    help_description = 'Get report data by  \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliResult, self).add_parser_args(child_parser)
        parser_argument_builder.add_sha256_argument()
        parser_argument_builder.add_environment_id_argument()
        parser_argument_builder.add_file_type_argument()
        parser_argument_builder.add_cli_output_argument()

    def save_files(self):
        file_type = self.given_args['type']
        api_response = self.api_object.api_response

        f_out_name = self.cli_output_folder + '/VxStream_{}.{}'.format(self.given_args['sha256'], file_type)
        if file_type == 'memory':
            f_out_name += '.zip'

        if file_type in ['xml', 'html', 'bin', 'pcap']:
            f_out = open(f_out_name, 'wb')
            try:
                gzip_file_handle = gzip.GzipFile(fileobj=BytesIO(api_response.content))
                f_out.write(gzip_file_handle.read())
            except Exception as e:
                f_out = open(f_out_name, 'wb')
                f_out.write(api_response.content)
                f_out.close()
            f_out.close()
        else:
            f_out = open(f_out_name, 'wb')
            f_out.write(api_response.content)
            f_out.close()

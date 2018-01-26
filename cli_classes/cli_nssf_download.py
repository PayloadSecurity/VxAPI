from cli_classes.cli_file_saver import CliFileSaver

import os

class CliNssfDownload(CliFileSaver):

    help_description = 'Get NSSF samples by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliNssfDownload, self).add_parser_args(child_parser)
        parser_argument_builder.add_file_with_nssf_list()
        parser_argument_builder.add_cli_output_argument()

    def attach_args(self, args):
        with args['hash_list'] as file:
            hashes = file.read().splitlines()

            if not hashes:
                raise Exception('Given file does not contain any data.')

            for key, value in enumerate(hashes):
                args['hashes[{}]'.format(key)] = value

        del args['hash_list']

        super(CliNssfDownload, self).attach_args(args)

    def save_files(self):
        api_response = self.api_object.api_response
        filename = self.api_object.api_response.headers['Vx-Filename']
        filename_without_extension, file_extension = os.path.splitext(filename)

        f_out_name = '{}/{}'.format(self.cli_output_folder, '{}_{}{}'.format(filename_without_extension, self.get_date_string(), file_extension))
        f_out = open(f_out_name, 'wb')
        f_out.write(api_response.content)
        f_out.close()


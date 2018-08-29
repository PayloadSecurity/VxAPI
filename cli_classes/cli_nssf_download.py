from cli.wrappers.cli_caller import CliCaller

import os
import gzip


class CliNssfDownload(CliCaller):

    help_description = 'Get NSSF samples by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliNssfDownload, self).add_parser_args(child_parser)
        parser_argument_builder.add_file_with_hash_list_arg()
        parser_argument_builder.add_cli_output_argument()

    def attach_args(self, args):
        super(CliNssfDownload, self).attach_args(self.convert_file_hashes_to_array(args))

    def get_result_msg(self):
        if self.api_object.api_response.headers['Content-Type'] == 'text/html':
            raise IOError('Error has occurred. Probably too many files were attached and webservice was not able to serve them. Please check the logs there to resolve that issue.')

        return super(CliNssfDownload, self).get_result_msg()

    def save_files(self):
        dir = '{}/{}'.format(self.cli_output_folder, 'nssf_download_{}'.format(self.get_date_string()))
        os.makedirs(dir)

        api_response = self.api_object.api_response
        splitted_file = api_response.content.splitlines(True)
        boundary = splitted_file[0].decode('utf-8').strip()
        lines_of_files = []
        current_file = 0
        processing_file = False
        filename_identificator = 'filename="'
        size_of_filename_identificator = len(filename_identificator)
        for x, line in enumerate(splitted_file):
            try:
                string_from_line = line.decode('utf-8')  # content is mixed, we've got bytes and strings - all of them should be there
            except UnicodeDecodeError:
                continue
            position_of_filename = string_from_line.find(filename_identificator)
            if position_of_filename != -1:
                position_of_ending = string_from_line.find('"',position_of_filename + size_of_filename_identificator + 1)
                lines_of_files.append([string_from_line[(position_of_filename + size_of_filename_identificator):position_of_ending], None,None])

            if processing_file is True:
                if string_from_line.startswith(boundary):
                    lines_of_files[current_file][2] = x

                    if string_from_line.endswith('--'):
                        break
                    else:
                        current_file = current_file + 1
                        processing_file = False
            elif line.isspace():
                processing_file = True
                lines_of_files[current_file][1] = x + 1
                continue

        for x, line_data in enumerate(lines_of_files):
            filename = line_data[0]
            path_file = '{}/{}'.format(dir, filename)
            file_bytes = splitted_file[line_data[1]:line_data[2]]
            last_line = splitted_file[(line_data[2] - 1):line_data[2]][0]
            file_bytes[-1] = last_line.split(b'\r\n')[0] # removing new line chars from the last line
            f_out = open(path_file, 'wb')
            f_out.writelines(file_bytes)
            f_out.close()

            saved_file_filename_without_ext, saved_file_extension = os.path.splitext(filename)

            if saved_file_extension == '.gz':
                decompressed_file_path = '{}/{}'.format(dir, saved_file_filename_without_ext)
                gzip_f_in = gzip.GzipFile(path_file)
                f_out = open(decompressed_file_path, 'wb')
                f_out.write(gzip_f_in.read())
                f_out.close()
                os.remove(path_file)

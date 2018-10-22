from cli.wrappers.cli_caller import CliCaller
import base64
from cli.cli_file_writer import CliFileWriter


class CliReportScreenshots(CliCaller):

    help_description = 'Retrieve an array of screenshots from a report in the Base64 format by \'{}\''
    result_msg_for_files = '\n\nResponse from sample screenshots endpoint contain json with encoded strings. Screenshots were saved in the output folder ({}).'

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliReportScreenshots, self).add_parser_args(child_parser)
        parser_argument_builder.add_id_arg()
        parser_argument_builder.add_file_output_path_opt()

    def get_result_msg(self):
        parent_result_msg = super(CliReportScreenshots, self).get_result_msg()

        if self.api_object.if_request_success() is True and self.given_args['verbose'] is True:
            return parent_result_msg + ' ' + self.get_result_msg_for_files()

        return parent_result_msg

    def get_processed_output_path(self):
        path = super(CliReportScreenshots, self).get_processed_output_path()

        return '{}/{}'.format(path, self.get_specific_output_dir_name())

    def get_specific_output_dir_name(self):
        return '{}-{}'.format(self.action_name, self.given_args['id'])

    def do_post_processing(self):
        if self.api_object.if_request_success() is True:
            self.save_files()

    def save_files(self):
        output_path = '{}/{}'.format(self.cli_output_folder, self.get_specific_output_dir_name())

        CliFileWriter.create_dir_if_not_exists(output_path)
        api_response_json = self.api_object.get_response_json()

        for screenshot_data in api_response_json:
            CliFileWriter.write(output_path, screenshot_data['name'], base64.b64decode(screenshot_data['image']))

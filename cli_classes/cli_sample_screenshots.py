from cli_classes.cli_caller import CliCaller
import base64


class CliSampleScreenshots(CliCaller):

    help_description = 'Get sample screenshots by \'{}\''
    result_msg_for_files = '\n\nResponse from sample screenshots endpoint contain json with encoded strings. Screenshots were saved in the output folder ({}).'

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliSampleScreenshots, self).add_parser_args(child_parser)
        parser_argument_builder.add_sha256_argument()
        parser_argument_builder.add_environment_id_argument()
        parser_argument_builder.add_cli_output_argument()

    def do_post_processing(self):
        if self.api_object.get_response_status_code() == 200 and self.api_object.get_response_msg_success_nature() is True:
            self.create_output_dir()
            self.save_files()

    def get_result_msg(self):
        parent_result_msg = super(CliSampleScreenshots, self).get_result_msg()

        if self.given_args['verbose'] is True:
            return parent_result_msg + ' ' + self.get_result_msg_for_files()
        else:
            return parent_result_msg

    def save_files(self):
        api_response_json = self.api_object.get_response_json()

        for screenshotData in api_response_json['response']['screenshots']:
            f_out = open(self.cli_output_folder + '/' + screenshotData['name'], 'wb')
            f_out.write(base64.b64decode(screenshotData['image']))
            f_out.close()

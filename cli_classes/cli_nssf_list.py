from cli_classes.cli_caller import CliCaller


class CliNssfList(CliCaller):

    help_description = 'Get NSSF list by \'{}\''
    result_msg_for_files = 'Hashes from response were saved in the output folder ({}).'

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliNssfList, self).add_parser_args(child_parser)
        parser_argument_builder.add_hash_format_argument()
        parser_argument_builder.add_visibility_argument()
        parser_argument_builder.add_verdict_format_argument()
        parser_argument_builder.add_from_date_argument()
        parser_argument_builder.add_to_date_argument()
        parser_argument_builder.add_cli_output_argument()

    def get_result_msg(self):
        super(CliNssfList, self).get_result_msg()  # just to throw exception if needed
        response_json = self.api_object.get_response_json().get('response')

        return self.get_result_msg_for_files() if response_json else 'As response does not have any hashes, file was not saved.'

    def save_files(self):
        response_json = self.api_object.get_response_json().get('response')

        if response_json:
            f_out_name = self.cli_output_folder + '/nssf_list_{}.txt'.format(self.get_date_string())

            f_out = open(f_out_name, 'w')
            for item in response_json:
                f_out.write("{}\n".format(item))
            f_out.close()









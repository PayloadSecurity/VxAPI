from cli.wrappers.cli_caller import CliCaller
from cli.formatter.cli_json_formatter import CliJsonFormatter


class CliScanState(CliCaller):

    help_description = 'Return list of available scanners by \'{}\''

    def get_result_msg(self):
        parent_result_msg = super(CliScanState, self).get_result_msg()

        if self.api_object.if_request_success() is True and self.given_args['verbose'] is False:
            current_json = self.api_object.get_response_json()
            filtered_json = []
            for scan in current_json:
                if scan['available']:
                    filtered_json.append(scan)

            return CliJsonFormatter.format_to_pretty_string(filtered_json)

        return parent_result_msg

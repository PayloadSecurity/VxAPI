import datetime
import traceback
from colors import Color


class CliMsgPrinter:

    @staticmethod
    def print_call_info(cli_object):
        print(Color.control('Request was sent at ' + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
        print('Endpoint URL: {}'.format(cli_object.api_object.get_full_endpoint_url()))
        print('HTTP Method: {}'.format(cli_object.api_object.request_method_name.upper()))
        print('Sent GET params: {}'.format(cli_object.api_object.params))
        print('Sent POST params: {}'.format(cli_object.api_object.data))
        print('Sent files: {}'.format(cli_object.api_object.files))

    @staticmethod
    def print_error_info(e):
        print(Color.control('During the code execution, error has occurred. Please try again or contact the support.'))
        print(Color.error('Message: \'{}\'.').format(str(e)) + '\n')
        print(traceback.format_exc())

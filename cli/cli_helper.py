from colors import Color
from constants import MINIMAL_SUPPORTED_INSTANCE_VERSION


class CliHelper:

    @staticmethod
    def check_if_version_is_supported(args, current_version, server):
        if args['quiet'] is False and 'hybrid-analysis.com' not in server and current_version.split('-')[0] < MINIMAL_SUPPORTED_INSTANCE_VERSION:
            print(Color.warning('This version of VxAPI works best on VxWebService version {} (or above). Consider upgrading to ensure the flawless performance.'.format(MINIMAL_SUPPORTED_INSTANCE_VERSION)))


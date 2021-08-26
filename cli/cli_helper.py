from colors import Color
from constants import MINIMAL_SUPPORTED_INSTANCE_VERSION
import pkg_resources

class CliHelper:

    @staticmethod
    def check_if_version_is_supported(args, current_version, server):
        parsed_current_version = pkg_resources.parse_version(current_version.split('-')[0])
        minimal_supported_version = pkg_resources.parse_version(MINIMAL_SUPPORTED_INSTANCE_VERSION)

        if args['quiet'] is False and 'hybrid-analysis.com' not in server and parsed_current_version < minimal_supported_version:
            print(Color.warning('This version of VxAPI works best on VxWebService version {} (or above). Consider upgrading to ensure the flawless performance.'.format(MINIMAL_SUPPORTED_INSTANCE_VERSION)))


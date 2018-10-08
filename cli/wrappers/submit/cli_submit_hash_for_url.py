from cli.wrappers.cli_caller import CliCaller


class CliSubmitHashForUrl(CliCaller):

    help_description = 'Determine a SHA256 that an online file or URL submission will have when being processed by the system by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliSubmitHashForUrl, self).add_parser_args(child_parser)
        parser_argument_builder.add_url_arg('Url to check')

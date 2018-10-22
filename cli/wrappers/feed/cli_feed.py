from cli.wrappers.cli_caller import CliCaller


class CliFeed(CliCaller):

    help_description = 'Access a JSON feed (summary information) of reports generated over the last X days by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliFeed, self).add_parser_args(child_parser)
        parser_argument_builder.add_feed_days_arg()

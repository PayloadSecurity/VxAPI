from cli_classes.cli_caller import CliCaller


class CliFeed(CliCaller):

    help_description = 'Get feed by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliFeed, self).add_parser_args(child_parser)
        parser_argument_builder.add_days_argument()


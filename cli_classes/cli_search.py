from cli_classes.cli_caller import CliCaller
from cli_classes.cli_argument_builder import CliArgumentBuilder


class CliSearch(CliCaller):

    help_description = 'Search the webservice by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliSearch, self).add_parser_args(child_parser)
        parser_argument_builder.add_query_search_argument()

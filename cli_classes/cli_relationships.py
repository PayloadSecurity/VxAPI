from cli_classes.cli_caller import CliCaller


class CliRelationships(CliCaller):

    help_description = 'Get all children and parent for given hash \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliRelationships, self).add_parser_args(child_parser)
        parser_argument_builder.add_sha256_argument()

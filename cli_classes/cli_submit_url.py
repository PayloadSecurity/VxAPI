from cli_classes.cli_caller import CliCaller


# 'environmentId', 'user', 'nosharevt', 'nohashlookup', 'kernelmode', 'analyzeurl', 'actionscript', 'hybridanalysis', 'experimentalantievasion', 'scriptlogging', 'inputsampletampering', 'torenabledanalysis', 'customdatetime', 'customcmdline', 'customruntime', 'client'
class CliSubmitUrl(CliCaller):

    help_description = 'Submit url by \'{}\''

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliSubmitUrl, self).add_parser_args(child_parser)
        parser_argument_builder.add_analyze_url_argument()
        parser_argument_builder.add_environment_id_argument()
        parser_argument_builder.add_nosharevt_argument()
        parser_argument_builder.add_priority_argument()
        # TODO - think about which of available flags should be available by CLI.

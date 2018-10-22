from cli.wrappers.cli_caller import CliCaller
from cli.arguments_builders.demo_bulk_cli_arguments import DemoBulkCliArguments


class CliReportDemoBulk(CliCaller):

    help_description = 'Return an archive with a collection of samples by \'{}\''

    def build_argument_builder(self, child_parser):
        return DemoBulkCliArguments(child_parser)

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliReportDemoBulk, self).add_parser_args(child_parser)
        parser_argument_builder.add_report_demo_bulk_modify_hash_opt()
        parser_argument_builder.add_report_demo_bulk_av_min_opt()
        parser_argument_builder.add_report_demo_bulk_av_max_opt()
        parser_argument_builder.add_report_demo_bulk_look_back_size_opt()
        parser_argument_builder.add_file_output_path_opt()

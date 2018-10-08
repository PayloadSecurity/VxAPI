from cli.wrappers.cli_caller import CliCaller


class CliReportDemoBulk(CliCaller):

    help_description = 'Return an archive with a collection of samples by \'{}\''

    def add_parser_args(self, child_parser): # TODO - maybe we can move those used methods to separated class
        parser_argument_builder = super(CliReportDemoBulk, self).add_parser_args(child_parser)
        parser_argument_builder.add_report_demo_bulk_modify_hash_opt()
        parser_argument_builder.add_report_demo_bulk_av_min_opt()
        parser_argument_builder.add_report_demo_bulk_av_max_opt()
        parser_argument_builder.add_report_demo_bulk_look_back_size_opt()
        parser_argument_builder.add_file_output_path_opt()

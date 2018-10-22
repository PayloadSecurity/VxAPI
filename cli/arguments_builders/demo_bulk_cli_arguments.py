from cli.arguments_builders.default_cli_arguments import DefaultCliArguments


class DemoBulkCliArguments(DefaultCliArguments):

    def add_report_demo_bulk_modify_hash_opt(self):
        self.parser.add_argument('--modify-hash', '-mh', action='store_true', default=False, help='When set, will add null byte at the end of sample file')

        return self

    def add_report_demo_bulk_av_min_opt(self):
        self.parser.add_argument('--av-min', '-an', type=int, default=5, help='The minimum required AV detect')

        return self

    def add_report_demo_bulk_av_max_opt(self):
        self.parser.add_argument('--av-max', '-ax', type=int, default=15, help='The maximum required AV detect')

        return self

    def add_report_demo_bulk_look_back_size_opt(self):
        self.parser.add_argument('--look-back-size', '-lbs', type=int, default=400, help='Number of samples which will be fetched and filtered. Once you will get error message about problem with finding all samples, please increase that value')

        return self

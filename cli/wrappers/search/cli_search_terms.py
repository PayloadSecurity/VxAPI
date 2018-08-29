from cli.wrappers.cli_caller import CliCaller
from cli.arguments_builders.search_cli_arguments import SearchCliArguments


class CliSearchTerms(CliCaller):

    help_description = 'Search the database using given search terms by \'{}\''

    def build_argument_builder(self, child_parser):
        return SearchCliArguments(child_parser)

    def add_parser_args(self, child_parser):
        parser_argument_builder = super(CliSearchTerms, self).add_parser_args(child_parser)
        parser_argument_builder.add_search_term_filename_opt()
        parser_argument_builder.add_search_term_filetype_opt()
        parser_argument_builder.add_search_term_filetype_desc_opt()
        parser_argument_builder.add_search_term_env_id_opt()
        parser_argument_builder.add_search_term_country_opt()
        parser_argument_builder.add_search_term_verdict_opt()
        parser_argument_builder.add_search_term_av_detect_opt()
        parser_argument_builder.add_search_term_vx_family_opt()
        parser_argument_builder.add_search_term_tag_opt()
        parser_argument_builder.add_search_term_port_opt()
        parser_argument_builder.add_search_term_host_opt()
        parser_argument_builder.add_search_term_domain_opt()
        parser_argument_builder.add_search_term_url_opt()
        parser_argument_builder.add_search_term_similar_to_opt()
        parser_argument_builder.add_search_term_context_opt()
        parser_argument_builder.add_search_term_imp_hash_opt()
        parser_argument_builder.add_search_term_ssdeep_opt()
        parser_argument_builder.add_search_term_authentihash_opt()

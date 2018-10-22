import argparse
from cli.arguments_builders.default_cli_arguments import DefaultCliArguments


class SearchCliArguments(DefaultCliArguments):

    def add_search_term_filename_opt(self):
        self.parser.add_argument('--filename', type=str, help='Filename e.g. invoice.exe')

        return self

    def add_search_term_filetype_opt(self):
        self.parser.add_argument('--filetype', type=str, help='Filetype e.g. docx')

        return self

    def add_search_term_filetype_desc_opt(self):
        self.parser.add_argument('--filetype-desc', type=str, help='Filetype description e.g. PE32 executable')

        return self

    def add_search_term_env_id_opt(self):
        self.parser.add_argument('--env-id', type=int, help='Environment Id')

        return self

    def add_search_term_country_opt(self):
        self.parser.add_argument('--country', type=str, help='Country (3 digit ISO) e.g. swe')

        return self

    def add_search_term_verdict_opt(self):
        self.parser.add_argument('--verdict', type=int, help='Verdict', choices={1: 'whitelisted', 2: 'no verdict', 3: 'no specific threat', 4: 'suspicious', 5: 'malicious'})

        return self

    def add_search_term_av_detect_opt(self):
        def type_av_detect(value):
            if value.find('-'):
                values = value.split('-')
            else:
                values = [value]

            for iter_value in values:
                forced_int_value = int(iter_value)
                if forced_int_value < 0 or forced_int_value > 100:
                    raise argparse.ArgumentTypeError('{} is not a value between {} and {}'.format(iter_value, 0, 100))

            return value

        self.parser.add_argument('--av-detect', type=type_av_detect, help='AV Multiscan range e.g. 50-70 (min 0, max 100)')

        return self

    def add_search_term_vx_family_opt(self):
        self.parser.add_argument('--vx-family', type=str, help='AV Family Substring e.g. nemucod')

        return self

    def add_search_term_tag_opt(self):
        self.parser.add_argument('--tag', type=str, help='Hashtag e.g. ransomware')

        return self

    def add_search_term_date_from_opt(self):
        self.parser.add_argument('--date-to', type=str, help='Date from in format: ‘Y-m-d H:i’ e.g. 2018-09-28 15:30') # TODO - add some date validator here

        return self

    def add_search_term_date_to_opt(self):
        self.parser.add_argument('--date-from', type=str, help='Date to in format: ‘Y-m-d H:i’ e.g. 2018-09-28 15:30')

        return self

    def add_search_term_port_opt(self):
        self.parser.add_argument('--port', type=str, help='Port e.g. 8080')

        return self

    def add_search_term_host_opt(self):
        self.parser.add_argument('--host', type=str, help='Host e.g. 192.168.0.1')

        return self

    def add_search_term_domain_opt(self):
        self.parser.add_argument('--domain', type=str, help='Domain e.g. checkip.dyndns.org')

        return self

    def add_search_term_url_opt(self):
        self.parser.add_argument('--url', type=str, help='HTTP Request Substring e.g. example')

        return self

    def add_search_term_similar_to_opt(self):
        self.parser.add_argument('--similar-to', type=str, help='Similar Samples e.g. <sha266>')

        return self

    def add_search_term_context_opt(self):
        self.parser.add_argument('--context', type=str, help='Sample Context e.g. <sha266>')

        return self

    def add_search_term_imp_hash_opt(self):
        self.parser.add_argument('--imphash', type=str)

        return self

    def add_search_term_ssdeep_opt(self):
        self.parser.add_argument('--ssdeep', type=str)

        return self

    def add_search_term_authentihash_opt(self):
        self.parser.add_argument('--authentihash', type=str)

        return self

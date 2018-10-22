from cli.arguments_builders.default_cli_arguments import DefaultCliArguments
from cli.types.values_in_between_action import ValuesInBetweenAction


class SubmissionCliArguments(DefaultCliArguments):

    def add_submission_submit_name_opt(self):
        self.parser.add_argument('--submit-name', '-sn', type=str, help='Optional \'submission name\' field that will be used for file type detection and analysis')

        return self

    def add_submission_comment_opt(self):
        self.parser.add_argument('--comment', '-co', type=str, help='Add comment (e.g. #hashtag) to sample')

        return self

    def add_submission_no_share_third_party_opt(self):
        self.parser.add_argument('--no-share-third-party', '-nstp', help='When set to \'1\', the sample is never shared with any third party', type=int, choices=[1, 0], default=1)

        return self

    def add_submission_allow_community_access_opt(self):
        self.parser.add_argument('--allow-community-access', '-aca', choices=[1, 0], default=1, type=int, help='When set \'1\', the sample will be available for vetted users of the HA community or custom application server')

        return self

    def add_submission_no_hash_lookup(self):
        self.parser.add_argument('--no-hash-lookup', '-nhl', choices=[1, 0], type=int)

        return self

    def add_submission_action_script_opt(self):
        self.parser.add_argument('--action-script', '-ac', choices={1: 'default', 2: 'default_maxantievasion', 3: 'default_randomfiles', 4: 'default_randomtheme', 5: 'default_openie'}, type=int, help='Optional custom runtime action script')

        return self

    def add_submission_hybrid_analysis_opt(self):
        self.parser.add_argument('--hybrid-analysis', '-ha', choices=[1, 0], type=int, help='When set to \'0\', no memory dumps or memory dump analysis will take place')

        return self

    def add_submission_experimental_anti_evasion_opt(self):
        self.parser.add_argument('--experimental-anti-evasion', '-eae', choices=[1, 0], type=int, help='When set to \'1\', will set all experimental anti-evasion options of the Kernelmode Monitor')

        return self

    def add_submission_script_logging_opt(self):
        self.parser.add_argument('--script-logging', '-sl', choices=[1, 0], type=int, help='When set to \'1\', will set the in-depth script logging engine of the Kernelmode Monitor')

        return self

    def add_submission_input_sample_tampering_opt(self):
        self.parser.add_argument('--input-sample-tampering', '--ist', choices=[1, 0], type=int, help='When set to \'1\', will allow experimental anti-evasion options of the Kernelmode Monitor that tamper with the input sample')

        return self

    def add_submission_tor_enabled_analysis_opt(self):
        self.parser.add_argument('--tor-enabled-analysis', '-tea', choices=[1, 0], type=int, help='When set to \'1\', will route the network traffic for the analysis via TOR (if properly configured on the server)')

        return self

    def add_submission_offline_analysis_opt(self):
        self.parser.add_argument('--offline-analysis', '-oa', choices=[1, 0], type=int, help='When set to \'1\', will disable outbound network traffic for the guest VM (takes precedence over ‘tor-enabled-analysis’ if both are provided)')

        return self

    def add_submission_email_opt(self):
        self.parser.add_argument('--email', '-e', type=str, help='Optional E-Mail address that may be associated with the submission for notification')

        return self

    def add_submission_custom_date_time_opt(self):
        self.parser.add_argument('--custom-date-time', '-cdt', type=str, help='Optional custom date/time that can be set for the analysis system. Expected format: yyyy-MM-dd HH:mm')

        return self

    def add_submission_custom_cmd_line_opt(self):
        self.parser.add_argument('--custom-cmd-line', '-ccl', type=str, help='Optional commandline that should be passed to the analysis file')

        return self

    def add_submission_custom_run_time_opt(self):
        self.parser.add_argument('--custom-run-time', '-crt', type=int, help='Optional runtime duration (in seconds)',)

        return self

    def add_submission_client_opt(self):
        self.parser.add_argument('--client', '-cl', type=str, help='Optional ‘client’ field (see ‘vxClients’)')

        return self

    def add_submission_priority_opt(self):
        self.parser.add_argument('--priority', '-pr', type=ValuesInBetweenAction(), help='Optional priority value between 0 (default) and 100 (highest)')

        return self

    def add_submission_document_password_opt(self):
        self.parser.add_argument('--document-password', '-dp', type=str, help='Optional document password that will be used to fill-in Adobe/Office password prompts')

        return self

    def add_submission_environment_variable_opt(self):
        self.parser.add_argument('--environment-variable', '-ev', type=str, help='Optional system environment value. The value is provided in the format: name=value')

        return self

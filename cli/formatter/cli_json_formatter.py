import json


class CliJsonFormatter:

    @staticmethod
    def format_to_pretty_string(given_json):
        return json.dumps(given_json, indent=4, sort_keys=True, ensure_ascii=False)

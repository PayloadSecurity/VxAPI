class CliLimitsFormatter:

    @staticmethod
    def format(limits, limit_type):
        result = {}

        if not limits:
            return result

        if limit_type == 'query':
            result = {
                'available': limits['limits'],
                'used': limits['used'],
                'limit_reached': limits['limit_reached']
            }
        else:
            result = {
                'available': limits['total']['quota'],
                'used': limits['total']['used'],
                'limit_reached': limits['total']['quota_reached']
            }

        return result

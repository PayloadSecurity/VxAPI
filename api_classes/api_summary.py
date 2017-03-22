from api_classes.api_caller import ApiCaller


class ApiSummary(ApiCaller):
    endpoint_url = '/api/summary/:hash'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_GET

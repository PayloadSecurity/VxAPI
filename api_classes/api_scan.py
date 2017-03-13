from api_classes.api_caller import ApiCaller


class ApiScan(ApiCaller):
    endpoint_url = '/api/scan/:sha256'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_GET

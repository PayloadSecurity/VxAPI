from api_classes.api_caller import ApiCaller


class ApiState(ApiCaller):
    endpoint_url = '/api/state/:sha256'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_GET

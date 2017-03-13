from api_classes.api_caller import ApiCaller


class ApiApiKeyData(ApiCaller):
    endpoint_url = '/api/get-api-key-data'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_GET

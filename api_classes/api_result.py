from api_classes.api_caller import ApiCaller


class ApiResult(ApiCaller):
    endpoint_url = '/api/result/:sha256'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_GET
    api_expected_data_type = ApiCaller.CONST_EXPECTED_DATA_TYPE_FILE
    endpoint_auth_level = ApiCaller.CONST_API_AUTH_LEVEL_DEFAULT



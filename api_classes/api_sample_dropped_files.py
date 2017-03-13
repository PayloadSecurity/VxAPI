from api_classes.api_caller import ApiCaller


class ApiSampleDroppedFiles(ApiCaller):
    endpoint_url = '/api/sample-dropped-files/:sha256'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_GET
    api_expected_data_type = ApiCaller.CONST_EXPECTED_DATA_TYPE_FILE
    endpoint_auth_level = ApiCaller.CONST_API_AUTH_LEVEL_DEFAULT

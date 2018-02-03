from api_classes.api_caller import ApiCaller


class ApiNssfDownload(ApiCaller):
    endpoint_url = '/api/nssf/download'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_POST
    endpoint_auth_level = ApiCaller.CONST_API_AUTH_LEVEL_ELEVATED
    api_expected_data_type = ApiCaller.CONST_EXPECTED_DATA_TYPE_FILE

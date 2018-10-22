file_handler = open('tests/_data/archive-file.zip', 'rb')

scenarios = [
    {
        "url": "/key/current",
        "method": "get",
        "status_code": 200,
        "json": {"api_key": "111", "auth_level": 500, "auth_level_name": "elevated"},
        "headers": {
            "content-type": "application/json",
            "webservice-version": "8.10",
            "api-version": "2.2.0",
            "api-limits": {"limits": {"minute": 5, "hour": 200}, "used": {"minute": 0, "hour": 0}, "limit_reached": False},
            "submission-limits": {"total": {"used": {"hour": 0, "hour_unique": 0, "day": 0, "day_unique": 0, "week": 15, "week_unique": 0, "month": 25, "month_unique": 0, "omega": 302, "omega_unique": 125}, "quota": {"hour": 200, "month": 5000}, "available": {"hour": 200, "month": 4975}, "quota_reached": False}, "quota_reached": False}
        }
    },
    {
        "url": "/report/demo-bulk",
        "method": "get",
        "status_code": 200,
        "content": file_handler.read(),
        "headers": {
            "content-type": "application/octet-stream",
            "vx-filename": "archive-file.zip",
            "webservice-version": "8.10",
            "api-version": "2.2.0",
            "api-limits": {"limits": {"minute": 5, "hour": 200}, "used": {"minute": 0, "hour": 0}, "limit_reached": False}
        }
    }
]


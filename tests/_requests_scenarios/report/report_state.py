scenarios = [
    {
        "url": "/key/current",
        "method": "get",
        "status_code": 200,
        "json": {"api_key": "111", "auth_level": 100, "auth_level_name": "default"},
        "headers": {
            "content-type": "application/json",
            "webservice-version": "8.10",
            "api-version": "2.2.0",
            "api-limits": {"limits": {"minute": 5, "hour": 200}, "used": {"minute": 0, "hour": 0}, "limit_reached": False},
            "submission-limits": {"total": {"used": {"hour": 0, "hour_unique": 0, "day": 0, "day_unique": 0, "week": 15, "week_unique": 0, "month": 25, "month_unique": 0, "omega": 302, "omega_unique": 125}, "quota": {"hour": 200, "month": 5000}, "available": {"hour": 200, "month": 4975}, "quota_reached": False}, "quota_reached": False}
        }
    },
    {
        "url": "/report/test/state",
        "method": "get",
        "status_code": 200,
        "json": [{"doc": "first"}, {"doc": "second"}],
        "headers": {
            "content-type": "application/json",
            "webservice-version": "8.10",
            "api-version": "2.2.0",
            "api-limits": {"limits": {"minute": 5, "hour": 200}, "used": {"minute": 0, "hour": 0}, "limit_reached": False}
        }
    }
]

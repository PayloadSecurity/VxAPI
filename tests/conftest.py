import os
import json

os.environ['APP_ENV'] = 'test'
os.environ['TEST_CONFIG'] = json.dumps({
        'api_key': 'test_me_please',
        'server': 'mock://my-webservice-instance'
})

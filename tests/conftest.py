import os
import json

os.environ['APP_ENV'] = 'test'
os.environ['TEST_CONFIG'] = json.dumps({
        'api_key': '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b',
        'server': 'mock://my-webservice-instance'
})

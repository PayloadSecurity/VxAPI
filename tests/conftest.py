import os
import json

os.environ['VX_APP_ENV'] = 'test'
os.environ['VX_DISABLE_CACHING'] = '1'
os.environ['VX_TEST_CONFIG'] = json.dumps({
        'api_key': '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b',
        'server': 'mock://my-webservice-instance'
})

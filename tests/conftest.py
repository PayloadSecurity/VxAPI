import pytest
import subprocess
import os
import json

os.environ['APP_ENV'] = 'test'
os.environ['TEST_CONFIG'] = json.dumps({
        'api_key': 'test_me_please',
        'server': 'mock://my-webservice-instance'
})

@pytest.fixture
def run_command():
    def do_run(*args):
        args = ['python3', 'vxapi.py'] + list(args)
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        (output, _) = p.communicate()
        output = output.decode('utf-8')
        return [p.returncode, output]
    return do_run

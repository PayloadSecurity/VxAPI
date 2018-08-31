# content of test_pyconv.py

import pytest
import subprocess
import os
import json


# we reuse a bit of pytest's own testing machinery, this should eventually come
# from a separatedly installable pytest-cli plugin.
pytest_plugins = ["pytester"]

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
        return [p.returncode, output]
    return do_run

def test_query(run_command):
    os.environ['TEST_SCENARIO'] = '1'

    print(run_command('search_hash', 'test'))

    assert False is True


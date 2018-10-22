import os
import time
import json
import hashlib
import pytest

from base_test import BaseTest

pytest_plugins = ["pytester"]


class TestCache(BaseTest):

    cache_file_path = 'cache/current_key_6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b.json'

    def clear_cache(self):
        self.remove_dir_content('cache')

    def load_cache_file_example(self):
        file_handler = open('tests/_data/current_key_cache_file.json', 'r')

        return json.load(file_handler)

    def init_request_scenario(self, name):
        os.environ['VX_TEST_SCENARIO'] = name

    def save_default_cache_file(self, secs_to_subtract):
        example_cache_file_content = self.load_cache_file_example()

        example_cache_file_content['timestamp'] = int(time.time()) - secs_to_subtract
        fake_cache_file_handler = open(self.cache_file_path, 'w')
        fake_cache_file_handler.write(json.dumps(example_cache_file_content))
        fake_cache_file_handler.close()

    def get_current_hash_of_cache_file(self):
        fake_cache_file_handler = open(self.cache_file_path, 'rb')
        fake_cache_file_hash = hashlib.sha256(fake_cache_file_handler.read()).hexdigest()
        fake_cache_file_handler.close()

        return fake_cache_file_hash

    def test_help_call_without_cache(self, run_command):
        self.clear_cache()
        self.init_request_scenario('cache_1')

        run_command('-h')
        assert 'positional arguments:' in self.output

        assert not os.listdir('cache')

    def test_help_call_with_cache_1(self, run_command):
        self.clear_cache()
        os.environ['VX_DISABLE_CACHING'] = '0'
        self.init_request_scenario('cache_1')

        run_command('-h')
        assert len(os.listdir('cache')) == 1
        assert os.path.exists('cache/current_key_6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b.json')
        assert 'positional arguments:' in self.output
        self.clear_cache()
        os.environ['VX_DISABLE_CACHING'] = '1'

    @pytest.mark.parametrize("is_exhausted", [(False),(True)])
    def test_help_call_with_cache_2(self, run_command, is_exhausted):
        self.clear_cache()
        os.environ['VX_DISABLE_CACHING'] = '0'
        self.init_request_scenario('cache_1')

        self.save_default_cache_file(999999 if is_exhausted is True else 5)
        fake_cache_file_hash = self.get_current_hash_of_cache_file()

        run_command('-h')

        assert 'positional arguments:' in self.output
        assert len(os.listdir('cache')) == 1
        assert os.path.exists(self.cache_file_path)

        if is_exhausted is True:
            assert fake_cache_file_hash != self.get_current_hash_of_cache_file()
        else:
            assert fake_cache_file_hash == self.get_current_hash_of_cache_file()

        self.clear_cache()
        os.environ['VX_DISABLE_CACHING'] = '1'

    def test_cache_refresh(self, run_command):
        self.clear_cache()
        os.environ['VX_DISABLE_CACHING'] = '0'
        self.init_request_scenario('cache_1')

        self.save_default_cache_file(5)
        fake_cache_file_hash = self.get_current_hash_of_cache_file()

        run_command('key_get_current')

        self.see_response({'api_key': '111', 'auth_level': 100, 'auth_level_name': 'default'})
        assert len(os.listdir('cache')) == 1
        assert os.path.exists(self.cache_file_path)

        assert fake_cache_file_hash != self.get_current_hash_of_cache_file()
        self.clear_cache()
        os.environ['VX_DISABLE_CACHING'] = '1'

    def test_cache_not_refresh(self, run_command):
        self.clear_cache()
        os.environ['VX_DISABLE_CACHING'] = '0'
        self.init_request_scenario('cache_2')

        self.save_default_cache_file(5)
        fake_cache_file_hash = self.get_current_hash_of_cache_file()

        run_command('feed_get_latest')

        self.see_response({'pies': 'to'})
        assert len(os.listdir('cache')) == 1
        assert os.path.exists(self.cache_file_path)

        assert fake_cache_file_hash == self.get_current_hash_of_cache_file()
        self.clear_cache()
        os.environ['VX_DISABLE_CACHING'] = '1' # TODO - try to implement py.test unittester, which supports teardown classes. Then that part should be moved there


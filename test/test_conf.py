from os.path import dirname, join

from mycroft_bus_client import client_from_config

CONF_PATH = join(dirname(__file__), 'test.conf')


class TestConfigLoader:
    def test_load_default(self):
        client = client_from_config(file_path=CONF_PATH)
        assert client.config.ssl == True
        assert client.config.port == 4242
        assert client.config.route == 'hitchhike'
        assert client.config.host == 'meaning.com'

    def test_load_alt(self):
        client = client_from_config('alt', file_path=CONF_PATH)
        assert client.config.ssl == False
        assert client.config.port == 666
        assert client.config.route == 'of_evil'
        assert client.config.host == 'evil.com'

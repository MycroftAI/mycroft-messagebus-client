# Copyright 2019 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from unittest.mock import Mock

from pyee import ExecutorEventEmitter

from mycroft_bus_client import MessageBusClient, Message
from mycroft_bus_client.client import MessageWaiter, MessageCollector


WS_CONF = {
    'websocket': {
        "host": "testhost",
        "port": 1337,
        "route": "/core",
        "ssl": False
    }
}


class TestMessageBusClient:
    def test_build_url(self):
        url = MessageBusClient.build_url('localhost', 1337, '/core', False)
        assert url == 'ws://localhost:1337/core'
        ssl_url = MessageBusClient.build_url('sslhost', 443, '/core', True)
        assert ssl_url == 'wss://sslhost:443/core'

    def test_create_client(self):
        mc = MessageBusClient()
        assert mc.client.url == 'ws://0.0.0.0:8181/core'

    def test_create_client_default_executor(self):
        mc = MessageBusClient()
        assert type(mc.emitter) == ExecutorEventEmitter

    def test_create_client_custom_executor(self):
        mock_emitter = Mock()
        mc = MessageBusClient(emitter=mock_emitter)
        assert mc.emitter == mock_emitter


class TestMessageWaiter:
    def test_message_wait_success(self):
        bus = Mock()
        waiter = MessageWaiter(bus, 'delayed.message')
        bus.once.assert_called_with('delayed.message', waiter._handler)

        test_msg = Mock(name='test_msg')
        waiter._handler(test_msg)  # Inject response

        assert waiter.wait() == test_msg

    def test_message_wait_timeout(self):
        bus = Mock()
        waiter = MessageWaiter(bus, 'delayed.message')
        bus.once.assert_called_with('delayed.message', waiter._handler)

        assert waiter.wait(0.3) is None


class TestMessageCollector:
    def test_message_wait_success(self):
        bus = Mock()
        collector = MessageCollector(bus, Message('delayed.message'),
                                     min_timeout=0.0, max_timeout=2.0)

        test_register = Mock(name='test_register')
        test_register.data = {
            'query': collector.collect_id,
            'handler': 'test_handler1'
        }
        collector._register_handler(test_register)  # Inject response

        test_response = Mock(name='test_register')
        test_response.data = {
            'query': collector.collect_id,
            'handler': 'test_handler1'
        }
        collector._receive_response(test_response)

        assert collector.collect() == [test_response]

    def test_message_drop_invalid(self):
        bus = Mock()
        collector = MessageCollector(bus, Message('delayed.message'),
                                     min_timeout=0.0, max_timeout=2.0)

        valid_register = Mock(name='valid_register')
        valid_register.data = {
            'query': collector.collect_id,
            'handler': 'test_handler1'
        }
        invalid_register = Mock(name='invalid_register')
        invalid_register.data = {
            'query': 'asdf',
            'handler': 'test_handler1'
        }
        collector._register_handler(valid_register)  # Inject response
        collector._register_handler(invalid_register)  # Inject response

        valid_response = Mock(name='valid_register')
        valid_response.data = {
            'query': collector.collect_id,
            'handler': 'test_handler1'
        }
        invalid_response = Mock(name='invalid_register')
        invalid_response.data = {
            'query': 'asdf',
            'handler': 'test_handler1'
        }
        collector._receive_response(valid_response)
        collector._receive_response(invalid_response)
        assert collector.collect() == [valid_response]

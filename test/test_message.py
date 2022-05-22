from time import time
from unittest import TestCase

from mycroft_bus_client import Message
from mycroft_bus_client.message import dig_for_message


def get_message_standard(message):
    return dig_for_message()


def get_message_alt_name(msg):
    return dig_for_message()


def get_message_no_name(_):
    return dig_for_message()


class TestMessage(TestCase):
    def test_serialize_deserialize(self):
        """Assert that a serized message is recreated when deserialized."""
        source = Message('test_type',
                         data={'robot': 'marvin', 'android': 'data'},
                         context={'origin': 'earth'})
        msg_string = source.serialize()
        reassembled = Message.deserialize(msg_string)
        self.assertEqual(source.msg_type, reassembled.msg_type)
        self.assertEqual(source.data, reassembled.data)
        self.assertEqual(source.context, reassembled.context)

    def test_response(self):
        """Assert that the .response is added to the message type for response.
        """
        source = Message('test_type',
                         data={'robot': 'marvin', 'android': 'data'},
                         context={'origin': 'earth'})
        response_msg = source.response()
        self.assertEqual(response_msg.msg_type, "test_type.response")
        self.assertEqual(response_msg.data, {})
        self.assertEqual(response_msg.context, source.context)

    def test_reply(self):
        """Assert that the source and destination are swapped"""
        source = Message('test_type',
                         data={'robot': 'marvin', 'android': 'data'},
                         context={'source': 'earth',
                                  'destination': 'alpha centauri'})

        reply_msg = source.reply('reply_type')
        self.assertEqual(reply_msg.context["source"],
                         source.context["destination"])
        self.assertEqual(reply_msg.context["destination"],
                         source.context["source"])

        # assert that .response calls .reply internally as stated in docstrings
        response_msg = source.response()
        self.assertEqual(response_msg.context, reply_msg.context)

    def test_dig_for_message_simple(self):
        test_msg = Message("test message", {"test": "data"}, {"time": time()})
        self.assertEqual(test_msg, get_message_standard(test_msg))
        test_msg = Message("test message", {"test": "data"}, {"time": time()})
        self.assertEqual(test_msg, get_message_alt_name(test_msg))
        test_msg = Message("test message", {"test": "data"}, {"time": time()})
        self.assertEqual(test_msg, get_message_no_name(test_msg))

    def test_dig_for_message_nested(self):
        message = Message("test message", {"test": "data"}, {"time": time()})

        def simple_wrapper():
            return get_message_no_name(message)

        self.assertEqual(simple_wrapper(), message)

        message = Message("test message", {"test": "data"}, {"time": time()})

        def get_message():
            return dig_for_message()

        def wrapper_method(msg):
            self.assertEqual(msg, get_message())

        wrapper_method(message)

    def test_dig_for_message_invalid_type(self):
        # Message that should be ignored
        _ = Message("test message", {"test": "data"}, {"time": time()})

        def wrapper_method(_):
            return dig_for_message()
        self.assertIsNone(wrapper_method(dict()))

    def test_dig_for_message_no_method_call(self):
        # Message that should be ignored
        _ = Message("test message", {"test": "data"}, {"time": time()})
        self.assertIsNone(dig_for_message())

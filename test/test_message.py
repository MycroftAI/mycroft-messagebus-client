from unittest import TestCase

from mycroft_bus_client import Message


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

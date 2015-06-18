# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from copy import deepcopy

from django.conf import settings
from django.test import TestCase

from channels.backends.hipchat import HipChatChannel
from channels.exceptions import HttpError, ImproperlyConfigured


channels = settings.CHANNELS["CHANNELS"]
config = channels["channels.backends.hipchat.HipChatChannel"]


class HipChatChannelTestCase(TestCase):
    def setUp(self):
        self.channel = HipChatChannel(**config)

    def test_init(self):
        with self.assertRaises(TypeError):
            HipChatChannel(**{})

        with self.assertRaises(ImproperlyConfigured):
            conf = deepcopy(config)
            conf["color"] = "blue"
            HipChatChannel(**conf)

        with self.assertRaises(ImproperlyConfigured):
            conf = deepcopy(config)
            conf["notify"] = "true"
            HipChatChannel(**conf)

    def test_send(self):
        self.channel.send("Test message")

        self.channel.send("Test message with `color=green`.\n"
                          "https://www.hipchat.com/",
                          options={"hipchat": {"color": "green"}})

        self.channel.send("Test message with `message_format=text`.\n"
                          "https://www.hipchat.com/",
                          options={"hipchat": {"message_format": "text"}})

    def test_send_fail(self):
        conf = deepcopy(config)
        conf["token"] = "token"
        channel = HipChatChannel(**conf)

        with self.assertRaises(HttpError):
            channel.send("Test message", fail_silently=False)

        channel.send("Test message", fail_silently=True)

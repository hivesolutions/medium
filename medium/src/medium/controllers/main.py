#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Solutions Development
# Copyright (c) 2008-2017 Hive Solutions Lda.
#
# This file is part of Hive Solutions Development.
#
# Hive Solutions Development is confidential and property of Hive Solutions Lda.,
# its usage is constrained by the terms of the Hive Solutions
# Confidential Usage License.
#
# Hive Solutions Development should not be distributed under any circumstances,
# violation of this may imply legal action.
#
# If you have any questions regarding the terms of this license please
# refer to <http://www.hive.pt/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import colony

from .base import BaseController

mvc_utils = colony.__import__("mvc_utils")

class MainController(BaseController):

    fields_map = {}
    """ The map containing the field values, these
    should be a key to value association of strings """

    ticker_messages_list = []
    """ The list containing the ticker messages the
    strings contained in the list should be valid unicode """

    def __init__(self, plugin, system):
        BaseController.__init__(self, plugin, system)
        self.fields_map = {}
        self.ticker_messages_list = []

    @mvc_utils.serialize
    def index(self, request):
        self._template(
            request = request,
            partial_page = "general/index.html.tpl",
            fields_map = self.fields_map,
            ticker_messages = self.ticker_messages_list
        )

    @mvc_utils.serialize
    def field_serialized(self, request):
        stream_helper_controller = self.system.stream_helper_controller
        key = request.field("key", "invalid")
        value = request.field("value", "invalid")
        status = dict(key = key, value = value)
        result = self.serialize(request, status)
        stream_helper_controller.send_s(
            request,
            "medium/communication",
            "medium/field/set",
            result,
            channels = ("public",)
        )
        self.fields_map[key] = value

    @mvc_utils.serialize
    def message_serialized(self, request):
        stream_helper_controller = self.system.stream_helper_controller
        value = request.field("value", "invalid")
        type = request.field("type", "information")
        status = dict(value = value, type = type)
        result = self.serialize(request, status)
        stream_helper_controller.send_s(
            request,
            "medium/communication",
            "medium/message/new",
            result,
            channels = ("public",)
        )

    @mvc_utils.serialize
    def video_serialized(self, request):
        stream_helper_controller = self.system.stream_helper_controller
        video_id = request.field("video_id", "invalid")
        status = dict(video_id = video_id)
        result = self.serialize(request, status)
        stream_helper_controller.send_s(
            request,
            "medium/communication",
            "medium/video/new",
            result,
            channels = ("public",)
        )

    @mvc_utils.serialize
    def ticker_message_serialized(self, request):
        stream_helper_controller = self.system.stream_helper_controller
        value = request.field("value", "invalid")
        type = request.field("type", "information")
        sub_value = request.field("sub_value", "")
        status = dict(value = value, type = type, sub_value = sub_value)
        result = self.serialize(request, status)
        stream_helper_controller.send_s(
            request,
            "medium/communication",
            "medium/ticker_message/new",
            result,
            channels = ("public",)
        )
        self.ticker_messages_list.append(status)

    @mvc_utils.serialize
    def ticker_clear_serialized(self, request):
        stream_helper_controller = self.system.stream_helper_controller
        status = dict()
        result = self.serialize(request, status)
        stream_helper_controller.send_s(
            request,
            "medium/communication",
            "medium/ticker_message/clear",
            result,
            channels = ("public",)
        )
        self.ticker_messages_list = []

    @mvc_utils.serialize
    def register_serialized(self, request, parameters = {}):
        # creates a new connection and adds the print handler
        # to it so that it becomes verbose
        connection = self.new_connection(
            parameters,
            "medium/communication",
            channels = ("public",)
        )
        connection.add_print_handler()
        connection.add_apn_handler(
            "12007EF74A0E8518EAB44CA4922B49FD4002462AFB37D7D9890A7E02D81FD24B",
            key_file = "c:/apn_key.pem",
            cert_file = "c:/apn_cert.pem"
        )

        # retrieves the identifier of the connection that
        # was just created, to be sent to the client
        connection_id = connection.get_connection_id()

        # creates the status (map)
        status = dict(id = connection_id)
        self.serialize(request, status)

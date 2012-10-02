#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Solutions Development
# Copyright (C) 2008-2012 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import colony.libs.import_util

mvc_utils = colony.libs.import_util.__import__("mvc_utils")
controllers = colony.libs.import_util.__import__("controllers")

class MainController(controllers.Controller):
    """
    The medium main controller.
    """

    fields_map = {}
    """ The map containing the filed values """

    ticker_messages_list = []
    """ The list containing the ticker messages """

    def __init__(self, plugin, system):
        controllers.Controller.__init__(self, plugin, system)
        self.fields_map = {}
        self.ticker_messages_list = []

    @mvc_utils.serialize_exceptions("all")
    def handle_media_index(self, rest_request, parameters = {}):
        """
        Handles the given media index rest request.

        @type rest_request: RestRequest
        @param rest_request: The media index rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # processes the contents of the template file assigning the appropriate values to it
        template_file = self.retrieve_template_file("general.html.tpl", partial_page = "index_contents.html.tpl")
        template_file.assign("fields_map", self.fields_map)
        template_file.assign("ticker_messages", self.ticker_messages_list)
        self.process_set_contents(rest_request, template_file)

    @mvc_utils.serialize_exceptions("all")
    def handle_media_field_serialized(self, rest_request, parameters = {}):
        """
        Handles the given media field serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The media field serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[mvc_utils.SERIALIZER_VALUE]

        # retrieves the required controllers
        communication_helper_controller = self.system.communication_helper_controller

        # retrieves the key and value from the rest request
        key = self.get_field(rest_request, "key", "invalid")
        value = self.get_field(rest_request, "value", "invalid")

        # creates the status (map)
        status = {
            "key" : key,
            "value" : value
        }

        # serializes the status and sets it as the rest request contents
        serialized_status = serializer.dumps(status)
        self.set_contents(rest_request, serialized_status)

        # sends the serialized broadcast message
        communication_helper_controller.send_serialized_broadcast_message(parameters, "medium/communication", "medium/field/set", serialized_status)

        # sets the field in the fields map
        self.fields_map[key] = value

    def handle_media_field_json(self, rest_request, parameters = {}):
        """
        Handles the given media field json rest request.

        @type rest_request: RestRequest
        @param rest_request: The media field json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin
        json_plugin = self.plugin.json_plugin

        # sets the serializer in the parameters
        parameters[mvc_utils.SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle media field serialized method
        self.handle_media_field_serialized(rest_request, parameters)

    @mvc_utils.serialize_exceptions("all")
    def handle_media_message_serialized(self, rest_request, parameters = {}):
        """
        Handles the given media message serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The media message serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[mvc_utils.SERIALIZER_VALUE]

        # retrieves the required controllers
        communication_helper_controller = self.system.communication_helper_controller

        # retrieves the message and type from the rest request
        value = self.get_field(rest_request, "value", "invalid")
        type = self.get_field(rest_request, "type", "information")

        # creates the status (map)
        status = {
            "value" : value,
            "type" : type
        }

        # serializes status and sets it as the rest request contents
        serialized_status = serializer.dumps(status)
        self.set_contents(rest_request, serialized_status)

        # sends the serialized broadcast message
        communication_helper_controller.send_serialized_broadcast_message(parameters, "medium/communication", "medium/message/new", serialized_status)

    def handle_media_message_json(self, rest_request, parameters = {}):
        """
        Handles the given media message json rest request.

        @type rest_request: RestRequest
        @param rest_request: The media message json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin
        json_plugin = self.plugin.json_plugin

        # sets the serializer in the parameters
        parameters[mvc_utils.SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle media message serialized method
        self.handle_media_message_serialized(rest_request, parameters)

    @mvc_utils.serialize_exceptions("all")
    def handle_media_video_serialized(self, rest_request, parameters = {}):
        """
        Handles the given media video serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The media video serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[mvc_utils.SERIALIZER_VALUE]

        # retrieves the required controllers
        communication_helper_controller = self.system.communication_helper_controller

        # retrieves the video id from the rest request
        video_id = self.get_field(rest_request, "video_id", "invalid")

        # creates the status (map)
        status = {
            "video_id" : video_id
        }

        # serializes the status and sets it as the rest request contents
        serialized_status = serializer.dumps(status)
        self.set_contents(rest_request, serialized_status)

        # sends the serialized broadcast message
        communication_helper_controller.send_serialized_broadcast_message(parameters, "medium/communication", "medium/video/new", serialized_status)

    def handle_media_video_json(self, rest_request, parameters = {}):
        """
        Handles the given media video json rest request.

        @type rest_request: RestRequest
        @param rest_request: The media video json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin
        json_plugin = self.plugin.json_plugin

        # sets the serializer in the parameters
        parameters[mvc_utils.SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle media video serialized method
        self.handle_media_video_serialized(rest_request, parameters)

    @mvc_utils.serialize_exceptions("all")
    def handle_media_ticker_message_serialized(self, rest_request, parameters = {}):
        """
        Handles the given media ticker serialized message rest request.

        @type rest_request: RestRequest
        @param rest_request: The media ticker message serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[mvc_utils.SERIALIZER_VALUE]

        # retrieves the required controllers
        communication_helper_controller = self.system.communication_helper_controller

        # retrieves the value, sub value and type from the rest request
        value = self.get_field(rest_request, "value", "invalid")
        type = self.get_field(rest_request, "type", "information")
        sub_value = self.get_field(rest_request, "sub_value", "")

        # creates the status (map)
        status = {
            "value" : value,
            "type" : type,
            "sub_value" : sub_value
        }

        # serializes the status and sets it as the rest request contents
        serialized_status = serializer.dumps(status)
        self.set_contents(rest_request, serialized_status)

        # sends the serialized broadcast message
        communication_helper_controller.send_serialized_broadcast_message(parameters, "medium/communication", "medium/ticker_message/new", serialized_status)

        # adds the status to the ticker messages list
        self.ticker_messages_list.append(status)

    def handle_media_ticker_message_json(self, rest_request, parameters = {}):
        """
        Handles the given media ticker message json rest request.

        @type rest_request: RestRequest
        @param rest_request: The media ticker message json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin
        json_plugin = self.plugin.json_plugin

        # sets the serializer in the parameters
        parameters[mvc_utils.SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle media ticker message serialized method
        self.handle_media_ticker_message_serialized(rest_request, parameters)

    def handle_media_ticker_clear_serialized(self, rest_request, parameters = {}):
        """
        Handles the given media ticker serialized clear rest request.

        @type rest_request: RestRequest
        @param rest_request: The media ticker clear serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[mvc_utils.SERIALIZER_VALUE]

        # retrieves the required controllers
        communication_helper_controller = self.system.communication_helper_controller

        # creates the status (map)
        status = {}

        # serializes the status and sets it as the rest request contents
        serialized_status = serializer.dumps(status)
        self.set_contents(rest_request, serialized_status)

        # sends the serialized broadcast message
        communication_helper_controller.send_serialized_broadcast_message(parameters, "medium/communication", "medium/ticker_message/clear", serialized_status)

        # clears the status to the ticker messages list
        self.ticker_messages_list = []

    def handle_media_ticker_clear_json(self, rest_request, parameters = {}):
        """
        Handles the given media ticker clear json rest request.

        @type rest_request: RestRequest
        @param rest_request: The media ticker clear json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin
        json_plugin = self.plugin.json_plugin

        # sets the serializer in the parameters
        parameters[mvc_utils.SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle media ticker clear serialized method
        self.handle_media_ticker_clear_serialized(rest_request, parameters)

#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Solutions Development
# Copyright (C) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
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

    @mvc_utils.serialize
    def handle_index(self, rest_request, parameters = {}):
        """
        Handles the given index rest request.

        @type rest_request: RestRequest
        @param rest_request: The index rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # processes the contents of the template file assigning the
        # appropriate values to it
        template_file = self.retrieve_template_file(
            "general.html.tpl",
            partial_page = "index_contents.html.tpl"
        )
        template_file.assign("fields_map", self.fields_map)
        template_file.assign("ticker_messages", self.ticker_messages_list)
        self.process_set_contents(rest_request, template_file)

    @mvc_utils.serialize
    def handle_field_serialized(self, rest_request, parameters = {}):
        """
        Handles the given field serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The field serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[mvc_utils.SERIALIZER_VALUE]

        # retrieves the required controllers
        stream_helper_controller = self.system.stream_helper_controller

        # retrieves the key and value from the rest request
        key = self.get_field(rest_request, "key", "invalid")
        value = self.get_field(rest_request, "value", "invalid")

        # creates the status (map)
        status = {
            "key" : key,
            "value" : value
        }

        # serializes the status and sets it as the rest request contents
        # along with the mime type associated with the serializer
        serialized_status = serializer.dumps(status)
        mime_type = serializer.get_mime_type()
        self.set_contents(rest_request, serialized_status, content_type = mime_type)

        # sends the serialized message to the public
        # channel (non secure)
        stream_helper_controller.send_s(
            parameters,
            "medium/communication",
            "medium/field/set",
            serialized_status,
            channels = ("public",)
        )

        # sets the field in the fields map
        self.fields_map[key] = value

    def handle_field_json(self, rest_request, parameters = {}):
        """
        Handles the given field json rest request.

        @type rest_request: RestRequest
        @param rest_request: The field json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin sets it as the serializer
        # object for the current request then redirects the request
        # to the general serialized method
        json_plugin = self.plugin.json_plugin
        parameters[mvc_utils.SERIALIZER_VALUE] = json_plugin
        self.handle_field_serialized(rest_request, parameters)

    @mvc_utils.serialize
    def handle_message_serialized(self, rest_request, parameters = {}):
        """
        Handles the given message serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The message serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[mvc_utils.SERIALIZER_VALUE]

        # retrieves the required controllers
        stream_helper_controller = self.system.stream_helper_controller

        # retrieves the message and type from the rest request
        value = self.get_field(rest_request, "value", "invalid")
        type = self.get_field(rest_request, "type", "information")

        # creates the status (map)
        status = {
            "value" : value,
            "type" : type
        }

        # serializes the status and sets it as the rest request contents
        # along with the mime type associated with the serializer
        serialized_status = serializer.dumps(status)
        mime_type = serializer.get_mime_type()
        self.set_contents(rest_request, serialized_status, content_type = mime_type)

        # sends the serialized message to the public
        # channel (non secure)
        stream_helper_controller.send_s(
            parameters,
            "medium/communication",
            "medium/message/new",
            serialized_status,
            channels = ("public",)
        )

    def handle_message_json(self, rest_request, parameters = {}):
        """
        Handles the given message json rest request.

        @type rest_request: RestRequest
        @param rest_request: The message json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin sets it as the serializer
        # object for the current request then redirects the request
        # to the general serialized method
        json_plugin = self.plugin.json_plugin
        parameters[mvc_utils.SERIALIZER_VALUE] = json_plugin
        self.handle_message_serialized(rest_request, parameters)

    @mvc_utils.serialize
    def handle_video_serialized(self, rest_request, parameters = {}):
        """
        Handles the given video serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The video serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[mvc_utils.SERIALIZER_VALUE]

        # retrieves the required controllers
        stream_helper_controller = self.system.stream_helper_controller

        # retrieves the video id from the rest request
        video_id = self.get_field(rest_request, "video_id", "invalid")

        # creates the status (map)
        status = {
            "video_id" : video_id
        }

        # serializes the status and sets it as the rest request contents
        # along with the mime type associated with the serializer
        serialized_status = serializer.dumps(status)
        mime_type = serializer.get_mime_type()
        self.set_contents(rest_request, serialized_status, content_type = mime_type)

        # sends the serialized message to the public
        # channel (non secure)
        stream_helper_controller.send_s(
            parameters,
            "medium/communication",
            "medium/video/new",
            serialized_status,
            channels = ("public",)
        )

    def handle_video_json(self, rest_request, parameters = {}):
        """
        Handles the given video json rest request.

        @type rest_request: RestRequest
        @param rest_request: The video json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin sets it as the serializer
        # object for the current request then redirects the request
        # to the general serialized method
        json_plugin = self.plugin.json_plugin
        parameters[mvc_utils.SERIALIZER_VALUE] = json_plugin
        self.handle_video_serialized(rest_request, parameters)

    @mvc_utils.serialize
    def handle_ticker_message_serialized(self, rest_request, parameters = {}):
        """
        Handles the given ticker serialized message rest request.

        @type rest_request: RestRequest
        @param rest_request: The ticker message serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[mvc_utils.SERIALIZER_VALUE]

        # retrieves the required controllers
        stream_helper_controller = self.system.stream_helper_controller

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
        # along with the mime type associated with the serializer
        serialized_status = serializer.dumps(status)
        mime_type = serializer.get_mime_type()
        self.set_contents(rest_request, serialized_status, content_type = mime_type)

        # sends the serialized message to the public
        # channel (non secure)
        stream_helper_controller.send_s(
            parameters,
            "medium/communication",
            "medium/ticker_message/new",
            serialized_status,
            channels = ("public",)
        )

        # adds the status to the ticker messages list
        self.ticker_messages_list.append(status)

    def handle_ticker_message_json(self, rest_request, parameters = {}):
        """
        Handles the given ticker message json rest request.

        @type rest_request: RestRequest
        @param rest_request: The ticker message json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin sets it as the serializer
        # object for the current request then redirects the request
        # to the general serialized method
        json_plugin = self.plugin.json_plugin
        parameters[mvc_utils.SERIALIZER_VALUE] = json_plugin
        self.handle_ticker_message_serialized(rest_request, parameters)

    @mvc_utils.serialize
    def handle_ticker_clear_serialized(self, rest_request, parameters = {}):
        """
        Handles the given ticker clear serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The ticker clear serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[mvc_utils.SERIALIZER_VALUE]

        # retrieves the required controllers
        stream_helper_controller = self.system.stream_helper_controller

        # creates the status (map)
        status = {}

        # serializes the status and sets it as the rest request contents
        # along with the mime type associated with the serializer
        serialized_status = serializer.dumps(status)
        mime_type = serializer.get_mime_type()
        self.set_contents(rest_request, serialized_status, content_type = mime_type)

        # sends the serialized message to the public
        # channel (non secure)
        stream_helper_controller.send_s(
            parameters,
            "medium/communication",
            "medium/ticker_message/clear",
            serialized_status,
            channels = ("public",)
        )

        # clears the status to the ticker messages list
        self.ticker_messages_list = []

    def handle_ticker_clear_json(self, rest_request, parameters = {}):
        """
        Handles the given ticker clear json rest request.

        @type rest_request: RestRequest
        @param rest_request: The ticker clear json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin sets it as the serializer
        # object for the current request then redirects the request
        # to the general serialized method
        json_plugin = self.plugin.json_plugin
        parameters[mvc_utils.SERIALIZER_VALUE] = json_plugin
        self.handle_ticker_clear_serialized(rest_request, parameters)

    @mvc_utils.serialize
    def handle_register_serialized(self, rest_request, parameters = {}):
        """
        Handles the given register serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The register serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[mvc_utils.SERIALIZER_VALUE]

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
        status = {
            "id" : connection_id
        }

        # serializes the status and sets it as the rest request contents
        # along with the mime type associated with the serializer
        serialized_status = serializer.dumps(status)
        mime_type = serializer.get_mime_type()
        self.set_contents(rest_request, serialized_status, content_type = mime_type)

    def handle_register_json(self, rest_request, parameters = {}):
        """
        Handles the given register json rest request.

        @type rest_request: RestRequest
        @param rest_request: The register json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin sets it as the serializer
        # object for the current request then redirects the request
        # to the general serialized method
        json_plugin = self.plugin.json_plugin
        parameters[mvc_utils.SERIALIZER_VALUE] = json_plugin
        self.handle_register_serialized(rest_request, parameters)

#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Solutions Development
# Copyright (C) 2010 Hive Solutions Lda.
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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2010 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

class CommunicationHelperController:
    """
    The communication helper controller.
    """

    media_dashboard_plugin = None
    """ The media dashboard plugin """

    media_dashboard = None
    """ The media dashboard """

    def __init__(self, media_dashboard_plugin, media_dashboard):
        """
        Constructor of the class.

        @type media_dashboard_plugin: MediaDashboardPlugin
        @param media_dashboard_plugin: The media dashboard plugin.
        @type media_dashboard: MediaDashboard
        @param media_dashboard: The media dashboard.
        """

        self.media_dashboard_plugin = media_dashboard_plugin
        self.media_dashboard = media_dashboard

    def send_serialized_broadcast_message(self, parameters, connection_name, message_id, message_contents):
        # serializes the message using, sending the message id and the message contents
        serialized_message = self._get_serialized_message(message_id, message_contents)

        # sends the broadcast message
        self.send_broadcast_message(parameters, connection_name, serialized_message)

    def _get_serialized_message(self, message_id, message_contents):
        # retrieves the json plugin
        json_plugin = self.media_dashboard_plugin.json_plugin

        # creates the message map
        message_map = {}

        # sets the message attributes in the message map
        message_map["id"] = message_id
        message_map["contents"] = message_contents

        # serializes the message map using the json plugin
        serialized_message = json_plugin.dumps(message_map)

        # returns the serialized message
        return serialized_message

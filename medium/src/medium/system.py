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

MEDIA_DASHBOARD_RESOURCES_PATH = "media_dashboard/dashboard/resources"
""" The media dashboard resources path """

EXTRAS_PATH = MEDIA_DASHBOARD_RESOURCES_PATH + "/extras"
""" The extras path """

class MediaDashboard:
    """
    The media dashboard class.
    """

    media_dashboard_plugin = None
    """ The media dashboard plugin """

    def __init__(self, media_dashboard_plugin):
        """
        Constructor of the class.

        @type media_dashboard_plugin: MediaDashboardPlugin
        @param media_dashboard_plugin: The media dashboard plugin.
        """

        self.media_dashboard_plugin = media_dashboard_plugin

    def load_components(self):
        """
        Loads the main components models, controllers, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the web mvc utils plugin
        mvc_utils_plugin = self.media_dashboard_plugin.mvc_utils_plugin

        # creates the controllers and assigns them to the current instance
        mvc_utils_plugin.assign_controllers(self, self.media_dashboard_plugin)

    def unload_components(self):
        """
        Unloads the main components models, controllers, etc.
        This load should occur the earliest possible in the unloading process.
        """

        # retrieves the web mvc utils plugin
        mvc_utils_plugin = self.media_dashboard_plugin.mvc_utils_plugin

        # destroys the controllers, unregistering them from the internal structures
        mvc_utils_plugin.unassign_controllers(self)

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the web mvc service. The tuple should relate the route with the handler
        method/function.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as patterns,
        to the web mvc service.
        """

        return (
            (r"^media_dashboard/?$", self.main_controller.handle_media_index, "get"),
            (r"^media_dashboard/field$", self.main_controller.handle_media_field_json, "get", "json"),
            (r"^media_dashboard/message$", self.main_controller.handle_media_message_json, "get", "json"),
            (r"^media_dashboard/video$", self.main_controller.handle_media_video_json, "get", "json"),
            (r"^media_dashboard/ticker_message$", self.main_controller.handle_media_ticker_message_json, "get", "json"),
            (r"^media_dashboard/ticker_clear$", self.main_controller.handle_media_ticker_clear_json, "get", "json")
        )

    def get_communication_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as communication patterns,
        to the web mvc service. The tuple should relate the route with a tuple
        containing the data handler, the connection changed handler and the name
        of the connection.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as communication patterns,
        to the web mvc service.
        """

        return (
            (r"^media_dashboard/communication$", (self.communication_controller.handle_data, self.communication_controller.handle_connection_changed, "media_dashboard/communication")),
        )

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the web mvc service. The tuple should relate the route with the base
        file system path to be used.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as resource patterns,
        to the web mvc service.
        """

        # retrieves the plugin manager
        plugin_manager = self.media_dashboard_plugin.manager

        # retrieves the media dashboard plugin path
        media_dashboard_plugin_path = plugin_manager.get_plugin_path_by_id(self.media_dashboard_plugin.id)

        return (
            (r"^media_dashboard/resources/.+$", (media_dashboard_plugin_path + "/" + EXTRAS_PATH, "media_dashboard/resources")),
        )

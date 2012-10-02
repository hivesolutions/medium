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

import colony.base.plugin_system
import colony.base.decorators

class MediaDashboardPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Media Dashboard plugin.
    """

    id = "pt.hive.hive_development.plugins.media_dashboard"
    name = "Media Dashboard Plugin"
    short_name = "Media Dashboard"
    description = "The plugin that offers the media dashboard service"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/media_dashboard/dashboard/resources/baf.xml"
    }
    capabilities = [
        "web.mvc_service",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.web.mvc.utils", "1.x.x"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.json", "1.x.x")
    ]
    main_modules = [
        "media_dashboard.dashboard.media_dashboard_system"
    ]

    media_dashboard = None
    """ The media dashboard """

    web_mvc_utils_plugin = None
    """ The web mvc utils plugin """

    json_plugin = None
    """ The json plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import media_dashboard.dashboard.media_dashboard_system
        self.media_dashboard = media_dashboard.dashboard.media_dashboard_system.MediaDashboard(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        self.media_dashboard.load_components()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)
        self.media_dashboard.unload_components()

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the web mvc service. The tuple should relate the route with the handler
        method/function.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as patterns,
        to the web mvc service.
        """

        return self.media_dashboard.get_patterns()

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

        return self.media_dashboard.get_communication_patterns()

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the web mvc service. The tuple should relate the route with the base
        file system path to be used.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as resource patterns,
        to the web mvc service.
        """

        return self.media_dashboard.get_resource_patterns()

    def get_web_mvc_utils_plugin(self):
        return self.web_mvc_utils_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.web.mvc.utils")
    def set_web_mvc_utils_plugin(self, web_mvc_utils_plugin):
        self.web_mvc_utils_plugin = web_mvc_utils_plugin

    def get_json_plugin(self):
        return self.json_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.json")
    def set_json_plugin(self, json_plugin):
        self.json_plugin = json_plugin

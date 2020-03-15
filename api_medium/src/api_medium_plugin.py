#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Solutions Development
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import colony

class APIMediumPlugin(colony.Plugin):
    """
    he main class for the Medium API plugin
    """

    id = "pt.hive.cronus.plugins.api.medium"
    name = "Medium API"
    description = "The plugin that offers the Medium API"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "api.medium"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.client.http"),
        colony.PluginDependency("pt.hive.colony.plugins.misc.json")
    ]
    main_modules = [
        "api_medium"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import api_medium
        self.system = api_medium.APIMedium(self)

    def create_client(self, api_attributes):
        """
        Creates a client, with the given API attributes.

        :type api_attributes: Dictionary
        :param api_attributes: The API attributes to be used.
        :rtype: MediumClient
        :return: The created client.
        """

        return self.system.create_client(api_attributes)

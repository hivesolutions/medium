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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
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

EXCEPTION_VALUE = "exception"
""" The exception value """

MESSAGE_VALUE = "message"
""" The message value """

class ExceptionController:
    """
    The media dashboard exception controller.
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

    def handle_exception(self, rest_request, parameters = {}):
        """
        Handles an exception.

        @type rest_request: RestRequest
        @param rest_request: The rest request for which the exception occurred.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the exception parameters
        exception = parameters.get(EXCEPTION_VALUE)
        exception_message = exception.get(MESSAGE_VALUE)

        # processes the contents of the template file assigning the appropriate values to it
        template_file = self.retrieve_template_file("general.html.tpl", partial_page = "exception.html.tpl")
        template_file.assign("exception_message", exception_message)
        self.process_set_contents(rest_request, template_file)

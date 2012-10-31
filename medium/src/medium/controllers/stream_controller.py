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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import colony.libs.import_util

EXCEPTION_VALUE = "exception"
""" The exception value """

MESSAGE_VALUE = "message"
""" The message value """

mvc_utils = colony.libs.import_util.__import__("mvc_utils")
controllers = colony.libs.import_util.__import__("controllers")

class StreamController(controllers.Controller):
    """
    The medium (communication) stream controller.
    """

    def handle_data(self, request, parameters = {}):
        """
        Handles the given data communication request.

        @type request: Request
        @param request: The communication request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        pass

    def handle_changed(self, request, parameters = {}):
        """
        Handles the given (connection) changed communication request.

        @type request: Request
        @param request: The communication request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the name of the operation to be processed
        # resulting from a change in the communication system
        operation = parameters.get("operation", None)
        if not operation: return

        # uses the name of the operation to route the call properly
        # based on the prefix of the method
        method = getattr(self, "handle_" + operation)
        method(request, parameters)

    def handle_channel(self, request, parameters = {}):
        # retrieves the name of the channel for which the
        # authentication process must be executed
        channel = parameters.get("channel", None)

        # in case the current channel is part of the public
        # channels sequence returns immediately (allowed)
        if channel == "public": return

        # raises a runtime error indicating the problem in the
        # handling of the validation of the channel association
        raise RuntimeError("Problem while registering channel: '%s'" % channel)

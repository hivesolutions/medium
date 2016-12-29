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

controllers = colony.__import__("controllers")

class BaseController(controllers.Controller):

    def __init__(self, plugin, system):
        controllers.Controller.__init__(self, plugin, system)

    def validate(self, request, parameters, validation_parameters):
        return self.system.require_permissions(request, validation_parameters)

    def template_file(self, template = "general.html.tpl", *args, **kwargs):
        return self.retrieve_template_file(
            file_path = template,
            *args,
            **kwargs
        )

    def _template(self, assign_session = True, *args, **kwargs):
        return self.template(assign_session = assign_session, *args, **kwargs)

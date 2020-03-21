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

class APIMedium(colony.System):
    """
    The API Medium class.
    """

    def create_client(self, api_attributes, open_client = True):
        """
        Creates a client, with the given API attributes.

        In case the open client flag is set the client is
        immediately opened.

        :type api_attributes: Dictionary
        :param api_attributes: The API attributes to be used.
        :type open_client: bool
        :param open_client: If the client should be opened.
        :rtype: MediumClient
        :return: The created client.
        """

        # retrieves the client HTTP plugin
        client_http_plugin = self.plugin.client_http_plugin

        # retrieves the json plugin
        json_plugin = self.plugin.json_plugin

        # retrieves the Medium structure (if available)
        medium_structure = api_attributes.get("medium_structure", None)

        # creates a new Medium client with the given options and in
        # case the is meant to be open open the client
        medium_client = MediumClient(json_plugin, client_http_plugin, medium_structure)
        open_client and medium_client.open()

        # returns the Medium client
        return medium_client

class MediumClient(object):
    """
    The class that represents a Medium client connection.
    """

    json_plugin = None
    """ The json plugin """

    client_http_plugin = None
    """ The client HTTP plugin """

    medium_structure = None
    """ The Medium structure """

    http_client = None
    """ The HTTP client for the connection """

    def __init__(self, json_plugin = None, client_http_plugin = None, medium_structure = None):
        """
        Constructor of the class.

        :type json_plugin: JSONPlugin
        :param json_plugin: The json plugin.
        :type client_http_plugin: ClientHTTPPlugin
        :param client_http_plugin: The client HTTP plugin.
        :type medium_structure: MediumStructure
        :param medium_structure: The Medium structure.
        """

        self.json_plugin = json_plugin
        self.client_http_plugin = client_http_plugin
        self.medium_structure = medium_structure

    def open(self):
        """
        Opens the Medium client.
        """

        pass

    def close(self):
        """
        Closes the Medium client.
        """

        # in case an HTTP client is defined must close
        # it in accordance with the specification
        if self.http_client: self.http_client.close({})

    def generate_medium_structure(self, base_url, set_structure = True):
        """
        Generates a new Medium structure, for the given parameters.

        :type base_url: String
        :param base_url: The base URL of the Medium provider.
        """

        # constructs a new Medium structure
        medium_structure = MediumStructure(base_url)

        # in case the structure is meant to be set
        # sets the Medium structure
        if set_structure: self.set_medium_structure(medium_structure)

        # returns the Medium structure
        return medium_structure

    def set_field(self, key, value):
        """
        Sets the field for the given key and value.

        :type key: String
        :param key: The key to the field to be set.
        :type value: String
        :param value: The value of the field to be set.
        :rtype: Dictionary
        :return: The field information for the given field parameters.
        """

        # retrieves the base URL from the Medium structure and then
        # uses it to construct the retrieval URL by appending the
        # current action suffix
        base_url = self.medium_structure.base_url
        retrieval_url = base_url + "field.json"

        # start the parameters map and then sets both the
        # value and the type values in the parameters
        parameters = {}
        parameters["key"] = key
        parameters["value"] = value

        # fetches the retrieval URL with the given parameters retrieving
        # the json and then loads the value into the data structure
        json = self._fetch_url(retrieval_url, parameters)
        data = self.json_plugin.loads(json)

        # returns the data
        return data

    def set_field_json(self, key, value):
        """
        Sets the field for the given key and value.
        The given value is going to be serialized into
        json and then provided to the service.

        :type key: String
        :param key: The key to the field to be set.
        :type value: String
        :param value: The value of the field to be set.
        :rtype: Dictionary
        :return: The field information for the given field parameters.
        """

        # loads json retrieving the data
        value_json = self.json_plugin.dumps(value)

        # sets the filed retrieving the return value
        return_value = self.set_field(key, value_json)

        # returns the return value
        return return_value

    def set_message(self, value, type):
        """
        Sets the message for the given value and type.

        :type value: String
        :param value: The value of the message to be set.
        :type type: String
        :param type: The type of the message to be set.
        :rtype: Dictionary
        :return: The message information for the given message parameters.
        """

        # retrieves the base URL from the Medium structure and then
        # uses it to construct the retrieval URL by appending the
        # current action suffix
        base_url = self.medium_structure.base_url
        retrieval_url = base_url + "message.json"

        # start the parameters map and then sets both the
        # value and the type values in the parameters
        parameters = {}
        parameters["value"] = value
        parameters["type"] = type

        # fetches the retrieval URL with the given parameters retrieving
        # the json and then loads the value into the data structure
        json = self._fetch_url(retrieval_url, parameters)
        data = self.json_plugin.loads(json)

        # returns the data
        return data

    def get_medium_structure(self):
        """
        Retrieves the Medium structure.

        :rtype: MediumStructure
        :return: The Medium structure.
        """

        return self.medium_structure

    def set_medium_structure(self, medium_structure):
        """
        Sets the Medium structure.

        :type medium_structure: MediumStructure
        :param medium_structure: The Medium structure.
        """

        self.medium_structure = medium_structure

    def _build_url(self, base_url, parameters):
        """
        Builds the URL for the given URL and parameters.

        :type base_url: String
        :param base_url: The base URL to be used.
        :type parameters: Dictionary
        :param parameters: The parameters to be used for URL construction.
        :rtype: String
        :return: The built URL for the given parameters.
        """

        # retrieves the HTTP client
        http_client = self._get_http_client()

        # build the URL from the base URL
        url = http_client.build_url(base_url, "GET", parameters)

        # returns the built URL
        return url

    def _fetch_url(self, url, parameters = None, method = "GET"):
        """
        Fetches the given URL for the given parameters and using the given method.

        :type url: String
        :param url: The URL to be fetched.
        :type parameters: Dictionary
        :param parameters: The parameters to be used the fetch.
        :type method: String
        :param method: The method to be used in the fetch.
        :rtype: String
        :return: The fetched data.
        """

        # in case parameters is not defined must create a new
        # parameters map to be used
        if not parameters: parameters = {}

        # retrieves the HTTP client
        http_client = self._get_http_client()

        # fetches the URL retrieving the HTTP response and then
        # retrieves the received message as the contents response
        http_response = http_client.fetch_url(url, method, parameters, content_type_charset = "utf-8")
        contents = http_response.received_message

        # returns the contents
        return contents

    def _get_http_client(self):
        """
        Retrieves the HTTP client currently in use (in case it's created)
        if not created creates the HTTP client.

        :rtype: HTTPClient
        :return: The retrieved HTTP client.
        """

        # in case no HTTP client exists
        if not self.http_client:
            # creates the HTTP client parameters
            http_client_parameters = {
                "content_type_charset" : "utf-8"
            }

            # creates the HTTP client
            self.http_client = self.client_http_plugin.create_client(http_client_parameters)

            # opens the HTTP client
            self.http_client.open({})

        # returns the HTTP client
        return self.http_client

class MediumStructure(object):
    """
    The Medium structure class.
    """

    base_url = None
    """ The base URL of the Medium provider """

    def __init__(self, base_url):
        """
        Constructor of the class.

        :type base_url: String
        :param base_url: The base URL of the Medium provider.
        """

        self.base_url = base_url

    def get_base_url(self):
        """
        Retrieves the base URL.

        :rtype: String
        :return: The base URL.
        """

        return self.base_url

    def set_base_url(self, base_url):
        """
        Sets the base URL.

        :type base_url: String
        :param base_url: The base URL.
        """

        self.base_url = base_url

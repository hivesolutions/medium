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

__author__ = "João Magalhães <joamag@hive.pt>"
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

class ApiMedium(colony.System):
    """
    The api medium class.
    """

    def create_client(self, api_attributes, open_client = True):
        """
        Creates a client, with the given api attributes.

        In case the open client flag is set the client is
        immediately opened.

        :type api_attributes: Dictionary
        :param api_attributes: The api attributes to be used.
        :type open_client: bool
        :param open_client: If the client should be opened.
        :rtype: MediumClient
        :return: The created client.
        """

        # retrieves the client http plugin
        client_http_plugin = self.plugin.client_http_plugin

        # retrieves the json plugin
        json_plugin = self.plugin.json_plugin

        # retrieves the medium structure (if available)
        medium_structure = api_attributes.get("medium_structure", None)

        # creates a new medium client with the given options and in
        # case the is meant to be open open the client
        medium_client = MediumClient(json_plugin, client_http_plugin, medium_structure)
        open_client and medium_client.open()

        # returns the medium client
        return medium_client

class MediumClient(object):
    """
    The class that represents a medium client connection.
    """

    json_plugin = None
    """ The json plugin """

    client_http_plugin = None
    """ The client http plugin """

    medium_structure = None
    """ The medium structure """

    http_client = None
    """ The http client for the connection """

    def __init__(self, json_plugin = None, client_http_plugin = None, medium_structure = None):
        """
        Constructor of the class.

        :type json_plugin: JsonPlugin
        :param json_plugin: The json plugin.
        :type client_http_plugin: ClientHttpPlugin
        :param client_http_plugin: The client http plugin.
        :type medium_structure: MediumStructure
        :param medium_structure: The medium structure.
        """

        self.json_plugin = json_plugin
        self.client_http_plugin = client_http_plugin
        self.medium_structure = medium_structure

    def open(self):
        """
        Opens the medium client.
        """

        pass

    def close(self):
        """
        Closes the medium client.
        """

        # in case an http client is defined must close
        # it in accordance with the specification
        if self.http_client: self.http_client.close({})

    def generate_medium_structure(self, base_url, set_structure = True):
        """
        Generates a new medium structure, for the given parameters.

        :type base_url: String
        :param base_url: The base url of the medium provider.
        """

        # constructs a new medium structure
        medium_structure = MediumStructure(base_url)

        # in case the structure is meant to be set
        # sets the medium structure
        if set_structure: self.set_medium_structure(medium_structure)

        # returns the medium structure
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

        # retrieves the base url from the medium structure and then
        # uses it to construct the retrieval url by appending the
        # current action suffix
        base_url = self.medium_structure.base_url
        retrieval_url = base_url + "field.json"

        # start the parameters map and then sets both the
        # value and the type values in the parameters
        parameters = {}
        parameters["key"] = key
        parameters["value"] = value

        # fetches the retrieval url with the given parameters retrieving
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

        # retrieves the base url from the medium structure and then
        # uses it to construct the retrieval url by appending the
        # current action suffix
        base_url = self.medium_structure.base_url
        retrieval_url = base_url + "message.json"

        # start the parameters map and then sets both the
        # value and the type values in the parameters
        parameters = {}
        parameters["value"] = value
        parameters["type"] = type

        # fetches the retrieval url with the given parameters retrieving
        # the json and then loads the value into the data structure
        json = self._fetch_url(retrieval_url, parameters)
        data = self.json_plugin.loads(json)

        # returns the data
        return data

    def get_medium_structure(self):
        """
        Retrieves the medium structure.

        :rtype: MediumStructure
        :return: The medium structure.
        """

        return self.medium_structure

    def set_medium_structure(self, medium_structure):
        """
        Sets the medium structure.

        :type medium_structure: MediumStructure
        :param medium_structure: The medium structure.
        """

        self.medium_structure = medium_structure

    def _build_url(self, base_url, parameters):
        """
        Builds the url for the given url and parameters.

        :type base_url: String
        :param base_url: The base url to be used.
        :type parameters: Dictionary
        :param parameters: The parameters to be used for url construction.
        :rtype: String
        :return: The built url for the given parameters.
        """

        # retrieves the http client
        http_client = self._get_http_client()

        # build the url from the base url
        url = http_client.build_url(base_url, "GET", parameters)

        # returns the built url
        return url

    def _fetch_url(self, url, parameters = None, method = "GET"):
        """
        Fetches the given url for the given parameters and using the given method.

        :type url: String
        :param url: The url to be fetched.
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

        # retrieves the http client
        http_client = self._get_http_client()

        # fetches the url retrieving the http response and then
        # retrieves the received message as the contents response
        http_response = http_client.fetch_url(url, method, parameters, content_type_charset = "utf-8")
        contents = http_response.received_message

        # returns the contents
        return contents

    def _get_http_client(self):
        """
        Retrieves the http client currently in use (in case it's created)
        if not created creates the http client.

        :rtype: HttpClient
        :return: The retrieved http client.
        """

        # in case no http client exists
        if not self.http_client:
            # creates the http client parameters
            http_client_parameters = {
                "content_type_charset" : "utf-8"
            }

            # creates the http client
            self.http_client = self.client_http_plugin.create_client(http_client_parameters)

            # opens the http client
            self.http_client.open({})

        # returns the http client
        return self.http_client

class MediumStructure(object):
    """
    The medium structure class.
    """

    base_url = None
    """ The base url of the medium provider """

    def __init__(self, base_url):
        """
        Constructor of the class.

        :type base_url: String
        :param base_url: The base url of the medium provider.
        """

        self.base_url = base_url

    def get_base_url(self):
        """
        Retrieves the base url.

        :rtype: String
        :return: The base url.
        """

        return self.base_url

    def set_base_url(self, base_url):
        """
        Sets the base url.

        :type base_url: String
        :param base_url: The base url.
        """

        self.base_url = base_url

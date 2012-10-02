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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

DEFAULT_CHARSET = "utf-8"
""" The default charset """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

CONTENT_TYPE_CHARSET_VALUE = "content_type_charset"
""" The content type charset value """

FIELD_URL_SUFFIX = "field.json"
""" The suffix for the field url """

MESSAGE_URL_SUFFIX = "message.json"
""" The suffix for the message url """

class ServiceMediaDashboard:
    """
    The service media dashboard class.
    """

    service_media_dashboard_plugin = None
    """ The service media dashboard plugin """

    def __init__(self, service_media_dashboard_plugin):
        """
        Constructor of the class.

        @type service_media_dashboard_plugin: ServiceMediaDashboardPlugin
        @param service_media_dashboard_plugin: The service media dashboard plugin.
        """

        self.service_media_dashboard_plugin = service_media_dashboard_plugin

    def create_remote_client(self, service_attributes, open_client = True):
        """
        Creates a remote client, with the given service attributes.

        @type service_attributes: Dictionary
        @param service_attributes: The service attributes to be used.
        @type open_client: bool
        @param open_client: If the client should be opened.
        @rtype: MediaDashboardClient
        @return: The created remote client.
        """

        # retrieves the client http plugin
        client_http_plugin = self.service_media_dashboard_plugin.client_http_plugin

        # retrieves the json plugin
        json_plugin = self.service_media_dashboard_plugin.json_plugin

        # retrieves the media dashboard structure (if available)
        media_dashboard_structure = service_attributes.get("media_dashboard_structure", None)

        # creates a new media dashboard client with the given options
        media_dashboard_client = MediaDashboardClient(json_plugin, client_http_plugin, media_dashboard_structure)

        # in case the client is meant to be open
        # open the client
        open_client and media_dashboard_client.open()

        # returns the media dashboard client
        return media_dashboard_client

class MediaDashboardClient:
    """
    The class that represents a media dashboard client connection.
    """

    json_plugin = None
    """ The json plugin """

    client_http_plugin = None
    """ The client http plugin """

    media_dashboard_structure = None
    """ The media dashboard structure """

    http_client = None
    """ The http client for the connection """

    def __init__(self, json_plugin = None, client_http_plugin = None, media_dashboard_structure = None):
        """
        Constructor of the class.

        @type json_plugin: JsonPlugin
        @param json_plugin: The json plugin.
        @type client_http_plugin: ClientHttpPlugin
        @param client_http_plugin: The client http plugin.
        @type media_dashboard_structure: MediaDashboardStructure
        @param media_dashboard_structure: The media dashboard structure.
        """

        self.json_plugin = json_plugin
        self.client_http_plugin = client_http_plugin
        self.media_dashboard_structure = media_dashboard_structure

    def open(self):
        """
        Opens the media dashboard client.
        """

        pass

    def close(self):
        """
        Closes the media dashboard client.
        """

        # in case an http client is defined
        if self.http_client:
            # closes the http client
            self.http_client.close({})

    def generate_media_dashboard_structure(self, base_url, set_structure = True):
        """
        Generates a new media dashboard structure, for the given parameters.

        @type base_url: String
        @param base_url: The base url of the media dashboard provider.
        """

        # constructs a new media dashboard structure
        media_dashboard_structure = MediaDashboardStructure(base_url)

        # in case the structure is meant to be set
        if set_structure:
            # sets the media dashboard structure
            self.set_media_dashboard_structure(media_dashboard_structure)

        # returns the media dashboard structure
        return media_dashboard_structure

    def set_field(self, key, value):
        """
        Sets the field for the given key and value.

        @type key: String
        @param key: The key to the field to be set.
        @type value: String
        @param value: The value of the field to be set.
        @rtype: Dictionary
        @return: The field information for the given field parameters.
        """

        # retrieves the base url
        base_url = self.media_dashboard_structure.base_url

        # sets the retrieval url
        retrieval_url = base_url + FIELD_URL_SUFFIX

        # start the parameters map
        parameters = {}

        # sets the key
        parameters["key"] = key

        # sets the value
        parameters["value"] = value

        # fetches the retrieval url with the given parameters retrieving the json
        json = self._fetch_url(retrieval_url, parameters)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

        # returns the data
        return data

    def set_field_json(self, key, value):
        """
        Sets the field for the given key and value.
        The given value is going to be serialized into
        json and then provided to the service.

        @type key: String
        @param key: The key to the field to be set.
        @type value: String
        @param value: The value of the field to be set.
        @rtype: Dictionary
        @return: The field information for the given field parameters.
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

        @type value: String
        @param value: The value of the message to be set.
        @type type: String
        @param type: The type of the message to be set.
        @rtype: Dictionary
        @return: The message information for the given message parameters.
        """

        # retrieves the base url
        base_url = self.media_dashboard_structure.base_url

        # sets the retrieval url
        retrieval_url = base_url + MESSAGE_URL_SUFFIX

        # start the parameters map
        parameters = {}

        # sets the value
        parameters["value"] = value

        # sets the type
        parameters["type"] = type

        # fetches the retrieval url with the given parameters retrieving the json
        json = self._fetch_url(retrieval_url, parameters)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

        # returns the data
        return data

    def get_media_dashboard_structure(self):
        """
        Retrieves the media dashboard structure.

        @rtype: MediaDashboardStructure
        @return: The media dashboard structure.
        """

        return self.media_dashboard_structure

    def set_media_dashboard_structure(self, media_dashboard_structure):
        """
        Sets the media dashboard structure.

        @type media_dashboard_structure: MediaDashboardStructure
        @param media_dashboard_structure: The media dashboard structure.
        """

        self.media_dashboard_structure = media_dashboard_structure

    def _build_url(self, base_url, parameters):
        """
        Builds the url for the given url and parameters.

        @type base_url: String
        @param base_url: The base url to be used.
        @type parameters: Dictionary
        @param parameters: The parameters to be used for url construction.
        @rtype: String
        @return: The built url for the given parameters.
        """

        # retrieves the http client
        http_client = self._get_http_client()

        # build the url from the base urtl
        url = http_client.build_url(base_url, GET_METHOD_VALUE, parameters)

        # returns the built url
        return url

    def _fetch_url(self, url, parameters = None, method = GET_METHOD_VALUE):
        """
        Fetches the given url for the given parameters and using the given method.

        @type url: String
        @param url: The url to be fetched.
        @type parameters: Dictionary
        @param parameters: The parameters to be used the fetch.
        @type method: String
        @param method: The method to be used in the fetch.
        @rtype: String
        @return: The fetched data.
        """

        # in case parameters is not defined
        if not parameters:
            # creates a new parameters map
            parameters = {}

        # retrieves the http client
        http_client = self._get_http_client()

        # fetches the url retrieving the http response
        http_response = http_client.fetch_url(url, method, parameters, content_type_charset = DEFAULT_CHARSET)

        # retrieves the contents from the http response
        contents = http_response.received_message

        # returns the contents
        return contents

    def _get_http_client(self):
        """
        Retrieves the http client currently in use (in case it's created)
        if not created creates the http client.

        @rtype: HttpClient
        @return: The retrieved http client.
        """

        # in case no http client exists
        if not self.http_client:
            # creates the http client parameters
            http_client_parameters = {
                CONTENT_TYPE_CHARSET_VALUE : DEFAULT_CHARSET
            }

            # creates the http client
            self.http_client = self.client_http_plugin.create_client(http_client_parameters)

            # opens the http client
            self.http_client.open({})

        # returns the http client
        return self.http_client

class MediaDashboardStructure:
    """
    The media dashboard structure class.
    """

    base_url = None
    """ The base url of the media dashboard provider """

    def __init__(self, base_url):
        """
        Constructor of the class.

        @type base_url: String
        @param base_url: The base url of the media dashboard provider.
        """

        self.base_url = base_url

    def get_base_url(self):
        """
        Retrieves the base url.

        @rtype: String
        @return: The base url.
        """

        return self.base_url

    def set_base_url(self, base_url):
        """
        Sets the base url.

        @type base_url: String
        @param base_url: The base url.
        """

        self.base_url = base_url

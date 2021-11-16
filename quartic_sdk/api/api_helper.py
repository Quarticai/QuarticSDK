import requests
from quartic_sdk.utilities.configuration import Configuration
import quartic_sdk.utilities.constants as Constants


class APIHelper:
    """
    The class is the helper class which will be used for making the API calls
    """

    def __init__(self, host, username=None, password=None, oauth_token=None, cert_path=None, verify_ssl=None, gql_host=None):
        """
        Create API Client
        """
        self.configuration = Configuration.get_configuration(
            host, username, password, oauth_token, cert_path, verify_ssl, gql_host)

    def can_verify_ssl_certificate(self):
        """
        This method returns the value of verify that can be boolean or certificate path for ssl cerification
        """
        verify = self.configuration.verify_ssl
        if self.configuration.verify_ssl and self.configuration.cert_path:
            verify = self.configuration.cert_path
        return verify

    def call_api(self, url, method_type, path_params=[], query_params={}, body={}):
        """
        Call the API at the given url
        :param: url:
        :param: method_type:
        :param: path_params:
        :param: query_params:
        :param: body:
        """
        assert method_type in Constants.METHOD_TYPES

        http_method_function_mapping = {
            Constants.API_GET: self.__http_get_api,
            Constants.API_POST: self.__http_post_api,
            Constants.API_PATCH: self.__http_patch_api,
            Constants.API_PUT: self.__http_put_api,
            Constants.API_DELETE: self.__http_delete_api
        }

        response = http_method_function_mapping[method_type](url, path_params, query_params, body)
        response.raise_for_status()
        return response

    def _get_oauth_headers(self):
        """
        Get OAuth headers
        """
        return {
            "Authorization": "Bearer " + self.configuration.oauth_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def __http_get_api(self, url, path_params=[], query_params={}, body={}):
        """
        The method makes a GET call via the requests module
        :param: url:
        :param: path_params:
        :param: query_params:
        :param: body:
        """
        request_url = self.configuration.host + url
        for path_param in path_params:
            request_url += str(path_param) + "/"

        if self.configuration.auth_type == Constants.BASIC:
            return requests.get(
                request_url,
                auth=(self.configuration.username, self.configuration.password),
                params=query_params,
                verify=self.can_verify_ssl_certificate()
            )
        elif self.configuration.auth_type == Constants.OAUTH:
            headers = self._get_oauth_headers()
            return requests.get(
                request_url, params=query_params, headers=headers, verify=self.can_verify_ssl_certificate()
            )

    def __http_post_api(self, url, path_params=[], query_params={}, body={}):
        """
        The method makes a POST call via the requests module
        :param: url:
        :param: path_params:
        :param: query_params:
        :param: body:
        """
        request_url = self.configuration.host + url
        for path_param in path_params:
            request_url += str(path_param) + "/"
        if self.configuration.auth_type == Constants.BASIC:
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            return requests.post(
                request_url,
                auth=(self.configuration.username, self.configuration.password),
                json=body,
                headers=headers,
                params=query_params,
                verify=self.can_verify_ssl_certificate()
            )
        elif self.configuration.auth_type == Constants.OAUTH:
            headers = self._get_oauth_headers()
            return requests.post(
                request_url, params=query_params, json=body, headers=headers, verify=self.can_verify_ssl_certificate()
            )

    def __http_patch_api(self, url, path_params=[], query_params={}, body={}):
        """
        The method makes a PATCH call via the requests module
        :param: url:
        :param: path_params:
        :param: query_params:
        :param: body:
        """
        raise NotImplementedError

    def __http_put_api(self, url, path_params=[], query_params={}, body={}):
        """
        The method makes a PUT call via the requests module
        :param: url:
        :param: path_params:
        :param: query_params:
        :param: body:
        """
        raise NotImplementedError

    def __http_delete_api(self, url, path_params=[], query_params={}, body={}):
        """
        The method makes a DELETE call via the requests module
        :param: url:
        :param: path_params:
        :param: query_params:
        :param: body:
        """
        raise NotImplementedError

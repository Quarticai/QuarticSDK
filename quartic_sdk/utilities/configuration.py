"""
The given class implements the configuration details that need to be saved
with the APIClient to make the API calls
"""
import urllib3
from quartic_sdk.utilities.constants import OAUTH, BASIC


class Configuration:

    def __init__(self, host, username=None, password=None, oauth_token=None, cert_path=None, verify_ssl=True, gql_host=None):
        """
        Initialize the configuration
        :param host:
        :param username:
        :param password:
        :param oauth_token:
        :param verify_ssl:
        :param graphql server url
        """
        self.host = host
        if oauth_token:
            self.oauth_token = oauth_token
            self.auth_type = OAUTH
        elif username and password:
            self.auth_type = BASIC
            self.username = username
            self.password = password
            self.basic_token = self.get_basic_auth_token()
        else:
            raise Exception("Auth not provided")

        self.verify_ssl = verify_ssl
        self.cert_path = cert_path
        self.gql_host = gql_host or self.host

    def get_basic_auth_token(self):
        """
        Get HTTP basic authentication header (string).

        :return: The token for basic HTTP authentication.
        """
        return urllib3.util.make_headers(
            basic_auth=self.username + ':' + self.password
        ).get('authorization')

    @classmethod
    def get_configuration(cls, host, username=None, password=None, oauth_token=None, cert_path=None, verify_ssl=True, gql_host=None):
        """
        The method gets all the required params and returns the configuration details
        for making the API calls
        :param host: name of the host
        :param username: username of the user
        :param password: password of the user
        :param oauth_token: oauth token for authenticating requests
        :param cert_path: path of certificate
        :param verify_ssl: boolean value
        :param gql_host: graphql server url
        :return: Configuration object
        """
        return Configuration(host, username, password, oauth_token, cert_path, verify_ssl, gql_host)

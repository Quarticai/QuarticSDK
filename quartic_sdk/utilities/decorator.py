import json
import os

import requests

import quartic_sdk.utilities.constants as Constants
from pathlib import Path

TOKEN_FILE = os.getenv("TOKEN_FILE_PATH",Path.home() / ".quartic")


def save_token(token, user_identification_string):
    """
    Save a token to a file.

    This function creates the necessary directory structure and saves the provided token to a file.

    Args:
        token (str): The token to be saved.

    Returns:
        None

    Raises:
        None
    """
    os.makedirs(os.path.dirname(f'{TOKEN_FILE}/{user_identification_string}/token.txt'), exist_ok=True)
    # Save token
    with open(f'{TOKEN_FILE}/{user_identification_string}/token.txt', 'w') as token_file:
        token_file.write(token)

# Function to request a new token (You need to implement this)


def request_new_token(refresh_token, host):
    """
    Request a new access token using a refresh token.

    This function sends a request to the specified host's refresh token endpoint to obtain a new access token.
    It includes the provided refresh token in the request data.

    Args:
        refresh_token (str): The refresh token used to obtain a new access token. If None, the request will fail.
        host (str): The base URL of the host where the refresh token request will be sent.

    Returns:
        str: The new access token obtained from the response.

    Raises:
        PermissionError: If the refresh token has expired or if any other error occurs during the token request.
    """
    try:
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        if refresh_token:
            response = requests.post(
                url=f"{host}/api/token/refresh/",
                data={
                    "refresh": refresh_token,
                },
                headers=headers,
            )
            # Check if the login was successful
            if response.status_code == 401:
                # Extract the access token and refresh token from the response cookies
                raise PermissionError(
                    'Refresh token has expired. Please recreate APIClient')
        return response.json().get('access')
    except Exception as e:
        raise e

# Decorator function to handle token expiration and refresh


def authenticate_with_tokens(func):
    """
    Decorator to handle token expiration and refresh for API authentication.

    This decorator checks for the existence of a token file, reads the stored access token, and attempts
    to refresh the token if it has expired. It updates the token file with the new access token and retries
    the original API call with the refreshed token if necessary.

    Args:
        func (callable): The function to decorate.

    Returns:
        callable: The decorated function.

    Raises:
        Exception: If the token file does not exist or if any other error occurs during token management.
        PermissionError: If the access token is missing in the token file.
    """
    def wrapper(self, *args, **kwargs):
        try:
            # Check if the token file exists
            if not os.path.exists(f'{TOKEN_FILE}/{self.configuration.username}/token.txt'):
                raise Exception("Token file does not exist. ")

            # Read the stored token
            with open(f'{TOKEN_FILE}/{self.configuration.username}/token.txt', 'r') as token_file:
                token_dict = json.loads(token_file.read())

            # Extract access token from the token dictionary
            self.access_token = token_dict.get('access_token')

            if not self.access_token:
                raise PermissionError("Access token missing in token file.")

            # Call the decorated function
            response = func(self, *args, **kwargs)

            # Check the response status code
            if response.status_code == 401:
                # Access token is likely expired, attempt to refresh it
                self.access_token = request_new_token(
                    refresh_token=token_dict.get('refresh_token'),
                    host=self.configuration.host
                )  # Implement this method to refresh the access token
                if not self.access_token:
                    raise Exception("Failed to refresh access token.")

                # Update the stored access token in the token dictionary
                token_dict['access_token'] = self.access_token

                # Save the updated token dictionary back to the token file
                with open(f'{TOKEN_FILE}/{self.configuration.username}/token.txt', 'w') as new_token_file:
                    new_token_file.write(json.dumps(token_dict))

                # Retry the original API call with the new access token
                response = func(self, *args, **kwargs)

            return response
        except Exception as e:
            print("Error authenticating:", e)
            return None

    return wrapper

import json
import os

import requests

import quartic_sdk.utilities.constants as Constants


def save_token(token):
    # Save token
    with open(Constants.TOKEN_FILE, 'w') as token_file:
        token_file.write(token)

# Function to request a new token (You need to implement this)


def request_new_token(refresh_token, host):
    try:
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        if refresh_token:
            response = requests.post(
                url=host + Constants.REFRESH_TOKEN,
                method_type=Constants.API_POST,
                data={
                    "refresh": refresh_token,
                },
                headers=headers
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
    def wrapper(self, *args, **kwargs):
        try:
            # Check if the token file exists
            if not os.path.exists(Constants.TOKEN_FILE):
                raise Exception("Token file does not exist. ")

            # Read the stored token
            with open(Constants.TOKEN_FILE, 'r') as token_file:
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
                with open(Constants.TOKEN_FILE, 'w') as new_token_file:
                    new_token_file.write(json.dumps(token_dict))

                # Retry the original API call with the new access token
                response = func(self, *args, **kwargs)

            return response
        except Exception as e:
            print("Error authenticating:", e)
            return None

    return wrapper

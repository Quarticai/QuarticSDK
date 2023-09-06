import os
import jwt
import json
import time
import requests
from cryptography.fernet import Fernet
import quartic_sdk.utilities.constants as Constants

# Constants
QUARTIC_FOLDER = '.quartic'
CREDENTIALS_FILE = os.path.join(QUARTIC_FOLDER, 'credentials.txt')
TOKEN_FILE = os.path.join(QUARTIC_FOLDER, 'token.jwt')
THRESHOLD_SECONDS = 86400 # 1 day threshold in seconds 
KEY_FILE = os.path.join(QUARTIC_FOLDER, 'encryption_key.key')

# Function to read or generate an encryption key

def get_or_generate_encryption_key():
    if os.path.exists(KEY_FILE):
        # If the key file exists, read the key
        with open(KEY_FILE, 'rb') as key_file:
            encryption_key = key_file.read()
    else:
        # If the key file doesn't exist, generate a new key and save it
        encryption_key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(encryption_key)
    return encryption_key

# Encryption/Decryption functions (You need to implement these)

def encrypt_credentials(credentials, encryption_key):
    cipher_suite = Fernet(encryption_key)
    return cipher_suite.encrypt(credentials.encode())


def decrypt_credentials(encrypted_credentials, encryption_key):
    cipher_suite = Fernet(encryption_key)
    return cipher_suite.decrypt(encrypted_credentials).decode()

# Function to save encrypted user credentials and token

def save_credentials_and_token(username, password, token, encryption_key):
    # Encrypt credentials before saving
    encrypted_creds = encrypt_credentials(json.dumps(
        {'username': username, 'password': password}), encryption_key)
    os.makedirs(QUARTIC_FOLDER, exist_ok=True)

    # Save encrypted credentials
    with open(CREDENTIALS_FILE, 'wb') as creds_file:
        creds_file.write(encrypted_creds)

    # Save token
    with open(TOKEN_FILE, 'w') as token_file:
        token_file.write(token)

# Function to request a new token (You need to implement this)

def request_new_token(username, password, host, oauth_token=None, cert_path=None, verify_ssl=False, gql_host=None):
    try:
        from quartic_sdk.api.api_helper import APIHelper
        api_helper = APIHelper(
            host, username, password, oauth_token, cert_path, verify_ssl, gql_host)
        response = api_helper.call_api(
            url=Constants.LOGIN,
            method_type=Constants.API_POST,
            body={
                "username": username,
                "password": password
            }
        )
        # Check if the login was successful
        if response.status_code == 302:
            # Extract the access token and refresh token from the response cookies
            access_token = response.cookies.get('access_token')
            refresh_token = response.cookies.get('refresh_token')
        new_token = json.dumps({"access_token":access_token,"refresh_token":refresh_token})
        save_credentials_and_token(
            username, password, new_token, get_or_generate_encryption_key())
        return new_token
    except Exception as e:
        print("Error requesting new token:", e)
        return None

# Decorator function to handle token expiration, login, and password change

def authenticate_with_tokens(func):
    def wrapper(self,*args, **kwargs):
        try:
            # Check if the token file exists
            if not os.path.exists(TOKEN_FILE):
                print("Token file does not exist. Creating new credentials and token...")
                new_token = request_new_token(
                    username=self.configuration.username,
                    password=self.configuration.password,
                    host=self.configuration.host
                    )
                self.access_token = json.dumps(new_token)['access_token']
                with open(TOKEN_FILE, 'w') as new_token_file:
                    new_token_file.write(new_token)
            else:
                with open(TOKEN_FILE, 'r') as token_file:
                    token = token_file.read()
                    # Decode without verification
                    decoded_token = jwt.decode(json.loads(token)['access_token'], verify=False)
                    # Check if token is about to expire soon
                    if decoded_token['exp'] - time.time() < THRESHOLD_SECONDS:
                        # Read encrypted credentials
                        with open(CREDENTIALS_FILE, 'rb') as creds_file:
                            encrypted_creds = creds_file.read()
                            # Decrypt credentials using the encryption key
                            decrypted_creds = decrypt_credentials(
                                encrypted_creds, get_or_generate_encryption_key())
                            # Request a new token using decrypted credentials
                            new_token = request_new_token(
                                decrypted_creds['username'], decrypted_creds['password'])
                            self.access_token = json.dumps(new_token)['access_token']
                            # Update stored token
                            with open(TOKEN_FILE, 'w') as new_token_file:
                                new_token_file.write(new_token)
                    self.access_token = json.dumps(token)['access_token']
            return func(self,*args, **kwargs)
        except Exception as e:
            print("Error authenticating:", e)
            return None

    return wrapper

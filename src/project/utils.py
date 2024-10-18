""" Package level utility functions.

This module includes the functions that is needed in multiple places inside this package.

"""

import base64
import hashlib
import json
import os
import struct
from pathlib import Path
from typing import Optional

import boto3
import botocore
import requests
from dotenv import load_dotenv

load_dotenv()


def upload_to_spaces(file_buffer, directory: str, file_name: str, bucket_name: Optional[str] = os.getenv("BUCKET_NAME"),
                     acl: Optional[str] = 'public-read'):
    try:
        session = boto3.session.Session()
        client = session.client('s3',
                                endpoint_url=os.getenv("ENDPOINT"),
                                config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                                # Configures to use subdomain/virtual calling format.
                                region_name=os.getenv('REGION_NAME'),  # Use the region in your endpoint.
                                aws_access_key_id=os.getenv('ACCESS_KEY'),
                                aws_secret_access_key=os.getenv('SECRET_KEY'))

        # Step 3: Call the put_object command and specify the file to upload.
        client.put_object(Bucket=bucket_name,
                          # The path to the directory you want to upload the object to, starting with your Space name.
                          Key=f"{directory}/{file_name}",
                          # Object key, referenced whenever you want to access this file later.
                          Body=file_buffer,  # The object's contents.
                          ACL=acl,  # Defines Access-control List (ACL) permissions, such as private or public.

                          )
    except Exception as e:
        print(e)


def generate_salt(date, secret_key):
    # Create a deterministic salt based on the date and secret key
    return hashlib.sha256((date + secret_key).encode()).digest()[:16]


def encode_key(date):
    secret_key = os.getenv('APP_SECRET')

    # Convert date to integer (remove hyphens and treat as number)
    date_int = int(date.replace('-', ''))

    # Create a hash of the date and secret key
    hash_input = f"{date_int}{secret_key}".encode()
    hash_output = hashlib.sha256(hash_input).digest()

    # Use the first 4 bytes of the hash as an integer
    random_int = struct.unpack('!I', hash_output[:4])[0]

    # XOR the date integer with the random integer
    encoded_int = date_int ^ random_int

    # Combine the random_int and encoded_int
    combined = (random_int << 32) | encoded_int

    # Convert to base64
    encoded = base64.urlsafe_b64encode(combined.to_bytes(10, 'big')).decode()

    # Remove padding and return
    return encoded.rstrip('=')


def decode_key(encoded):
    # Add padding back if necessary
    encoded += '=' * ((4 - len(encoded) % 4) % 4)

    # Decode from base64
    decoded = int.from_bytes(base64.urlsafe_b64decode(encoded), 'big')

    # Extract random_int and encoded_int
    random_int = decoded >> 32
    encoded_int = decoded & 0xFFFFFFFF

    # XOR to get the original date integer
    date_int = encoded_int ^ random_int

    # Convert back to date string
    date = f"{date_int:08d}"
    date = f"{date[:4]}-{date[4:6]}-{date[6:]}"

    # Verify the result
    if encode_key(date) == encoded:
        return date
    else:
        return None


def date_encoded_filename(filepath, date):
    # Convert the filepath to a Path object
    path = Path(filepath)

    # Get the stem (filename without extension) and suffix (extension)
    stem = path.stem
    suffix = path.suffix

    # Get the key
    key = encode_key(date)

    # Create the new filename with the key inserted
    new_filename = f"{stem}_{key}{suffix}"

    # Return the new path with the modified filename
    return path.with_name(new_filename)


def send_to_wsj(msg: str, webhook: str = "uat"):
    """Post to an incoming webhook url.

    Parameters
    ----------
    msg : str
        The message that will post to the room.
    webhook : str, optional
        This selects which webhook url to use., by default 'uat'
    """
    url = ""
    if webhook == "uat":
        url = os.getenv("UAT")
    if webhook == "app":
        url = os.getenv("APP")
    if webhook == "steamroom":
        url = os.getenv("STEAMROOM")

    js = json.dumps({"message": msg})

    result = requests.post(url, js)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print(
            "Payload delivered successfully to wsj, code {}.".format(result.status_code)
        )


def next_trading_date():
    """
    Returns datetime object of the next trading date. Could check API and see.
    Returns
    -------

    """
    pass
    # T


if __name__ == "__main__":
    pass

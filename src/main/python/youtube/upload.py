
import config
from music.music_meta import MusicMeta
from files import file_utils

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
import logging as log

import socket

socket.setdefaulttimeout(config.YOUTUBE_SOCKET_TIMEOUT)

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = config.YOUTUBE_OAUTH_SECRET_FILE

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


# Authorize the request and store authorization credentials.
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)


def initialize_upload(youtube, file_meta: MusicMeta):
    body=dict(
        snippet=dict(
            title=file_utils.create_desc(file_meta),
            description=file_utils.create_desc(file_meta),
            tags=file_utils.create_tags(file_meta),
            categoryId=config.YOUTUBE_CATEGORY
        ),
        status=dict(
            privacyStatus=VALID_PRIVACY_STATUSES[0],
            madeForKids=True
        )
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(file_meta.path)
    )
    print('uploadig video...')
    response = insert_request.execute()

    print(response)


def upload_list(youtube, file_list, path: str):
    upload_success_path = file_utils.create_path([path, config.LOCATION_UPLOAD_SUCCESS])
    for file in file_list:
        try:
            initialize_upload(youtube, file)
            file_utils.move_file(file.path, upload_success_path)
            file_utils.move_file('.'.join([file.path, config.META_SUFFIX]), upload_success_path)
        except Exception as e:
            log.error('error while uploading video from {}'.format(file.path))
            log.error(e)



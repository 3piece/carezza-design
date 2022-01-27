from pathlib import Path
from boxsdk import OAuth2, Client
from subprocess import run
from json import loads
# import yaml
import logging

_logger = logging.getLogger(__name__)


class UploadToBox:
    # folder_id = '139438417628'  # back_ups
    folder_id = '139440183208'  # errors
    client_id = 'cem6bou667aiamfgtrgcrsutho7nt9hf'
    client_secret = 'Zx4dTFRyJH15RjoNntC1I1LAa7AG0BKx'

    module_path = '/home/odoo/src/user/cron_import/'
    script_path = f'{module_path}static/sh/'

    BASE_FOLDER = '/home/odoo/imports/origin/exports/'

    def upload(self, timestamp):
        if not timestamp:
            return "Please provide timestamp"

        result_json_string = run([f'{UploadToBox.script_path}get_access_token.sh'], capture_output=True,
                                 text=True).stdout

        result_json = loads(result_json_string)

        _logger.info(f'The new access token is: {result_json["access_token"]}')
        auth = OAuth2(
            client_id=UploadToBox.client_id,
            client_secret=UploadToBox.client_secret,
            access_token=result_json["access_token"]
        )

        client = Client(auth)
        source_folder = f'{UploadToBox.BASE_FOLDER}{timestamp}/'

        subfolder = client.folder(UploadToBox.folder_id).create_subfolder(timestamp)
        _logger.debug("uploaded to Box folder: %s", subfolder)
        for file_path in Path(source_folder).glob('*'):
            _logger.info(f'path: {file_path.parent} | file: {file_path.name}')
            new_file = client.folder(subfolder.id).upload(file_path)
            _logger.info('File "{0}" uploaded to Box with file ID {1}'.format(new_file.name, new_file.id))
        _logger.info(f'All files uploaded to Box folder: {subfolder}')

        #  get API App Access token using curl (no python func avialable). Not sure how long the expires is ~60 minutes. Can I use more than once - not sure?
        #  curl --location --request POST 'https://api.box.com/oauth2/token' --header 'content-type: application/x-www-form-urlencoded' --data-urlencode 'client_id=iu1g37vyi26a2xlymzvrzytj477mmmbc' --data-urlencode 'client_secret=zCmPNy7Fa0KL9KWERpKeiMgN1N5lTzLD' --data-urlencode 'grant_type=client_credentials' --data-urlencode 'box_subject_type=enterprise' --data-urlencode 'box_subject_id=833621239'
        #  example response: {"access_token":"kYs5HU34N10yPtj7JeGU4mVFKLedkw7b","expires_in":3751,"restricted_to":[],"token_type":"bearer"}

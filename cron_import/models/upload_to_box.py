
import yaml
from pathlib import Path
import logging
from boxsdk import OAuth2, Client


class UploadToBox:

    # folder_id = '139438417628'  # back_ups
    folder_id = '139440183208'  # errors

    auth = OAuth2(
        client_id='mflou9qn4cyey7bzgljc3idz5355zv25',
        client_secret='aBYsbJjKX5cfgbfc1znI4iMwRgukeHrj',
        access_token='fNbrXWbi7b7ElWafApcwAEvATMpqERFa'
    )

    # LOC_OUT = '../output_3/'
    # FILES_UP = 'po_error.log'
    # TEST_FILES = '/home/pi3ce/03_DevProjects/carezza_dev/carezza-design/import_assist/o_logs_out/220112-1645_2'

    BASE_FOLDER = '/home/odoo/imports/origin/exports/'


    def upload(self, timestamp):
        if not timestamp:
            return "Please provide timestamp"
        client = Client(UploadToBox.auth)
        source_folder = f'{UploadToBox.BASE_FOLDER}{timestamp}'

        #subfolder = client.folder('0').create_subfolder('My Stuff')
        # new_file = client.folder(folder_id).upload('/home/pi3ce/03_DevProjects/carezza/carezza-design/import_assist/origin/odoo_po_import_3.csv')
        # new_file = client.folder(folder_id).upload('/home/pi3ce/03_DevProjects/carezza/carezza-design/import_assist/output_2/error_log_po_lines.log')
        # new_file = client.folder(folder_id).upload('/home/pi3ce/03_DevProjects/carezza/carezza-design/import_assist/output_2/purchase.order.lines.M.csv.fail')
        # new_file = client.folder(folder_id).upload(LOC_OUT + FILES_UP)
        subfolder = client.folder(UploadToBox.folder_id).create_subfolder(timestamp)
        for file_path in Path(source_folder).glob('*'):
            print(f'path: {file_path.parent} | file: {file_path.name}')
            new_file = client.folder(subfolder).upload(file_path)
            print('File "{0}" uploaded to Box with file ID {1}'.format(new_file.name, new_file.id))
        print(f'All files uploaded to Box folder: {subfolder}')
        #  get API App Access token using curl (no python func avialable). Not sure how long the expires is ~60 minutes. Can I use more than once - not sure?
        #  curl --location --request POST 'https://api.box.com/oauth2/token' --header 'content-type: application/x-www-form-urlencoded' --data-urlencode 'client_id=iu1g37vyi26a2xlymzvrzytj477mmmbc' --data-urlencode 'client_secret=zCmPNy7Fa0KL9KWERpKeiMgN1N5lTzLD' --data-urlencode 'grant_type=client_credentials' --data-urlencode 'box_subject_type=enterprise' --data-urlencode 'box_subject_id=833621239'
        #  example response: {"access_token":"kYs5HU34N10yPtj7JeGU4mVFKLedkw7b","expires_in":3751,"restricted_to":[],"token_type":"bearer"}


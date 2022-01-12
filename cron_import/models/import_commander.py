
import argparse
from pathlib import Path
from subprocess import run
from shutil import move
from datetime import datetime, timedelta


from convert_po import convert_data
from process_records import OdooProcessor
# def move_file(input_foldeder, input_file, output_folder):
#
#     return True
#
# def archive_files(input_foldeder, input_files, output_folder):
#     for file in input_files:
#         move_file(input_foldeder, file, output_folder)
#     return True

# python ./import_commander.py -i ../origin/source_files/ -o ../output_3/

def run_stack():
    processor = OdooProcessor()
    po_suffix = 'po'
    receipts_suffix = 'rcpt'
    timestamp = (datetime.now() + timedelta(hours=1)).strftime("%y%m%d-%H%M")
    export_list = []
    root_path = '/home/odoo/imports/'
    # lib_path = f'{root_path}lib/'
    input_path = f'{root_path}origin/source_files/'
    processed_dir = f'{input_path}processed/'
    working_path = f'{root_path}origin/working/'
    module_path = '/home/odoo/src/user/cron_import/'
    script_path = f'{module_path}static/sh/'
    
    run(f'{script_path}download_box_file.sh')

    # get filename(s)
    proc_pos = False
    for file_path in Path(input_path).glob(f'{po_suffix}*.csv'):
        print(f'path: {file_path.parent} | file: {file_path.name}')
        success = convert_po.convert_data(str(file_path), output_folder=working_path)
        if success:
    #     # if True:
            run(f'{script_path}purchase_order.sh')
            proc_pos = True
            f_input = Path(f'{input_path}{file_path.name}')
            f_output = Path(f'{processed_dir}{timestamp}-{file_path.stem}.csv')
            print(f'input: {f_input} | output: {f_output}')
            move(f_input, f_output)
            export_list.append(f_output)

    print('checking proc process: %s', proc_pos)
    # if True:
    if proc_pos:
        print('Processing pos')
        try:
            processor = OdooProcessor()
            processor.process_pos()
        except Exception as e:
            print(f"Failed to process PO's: {e}")
        print('closing pos')
        # run(f'{args.output}purchase_order_status_done.sh')
        run(f'{script_path}move_logs.sh')

    print(export_list)
    print("--== FINISHED ==--")

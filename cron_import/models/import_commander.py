
import argparse
from pathlib import Path
from subprocess import run
from shutil import move
from datetime import datetime, timedelta


from .convert_po import convert_data
from .process_records import OdooProcessor
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
    processed_dir = 'processed/'
    timestamp = (datetime.now() + timedelta(hours=1)).strftime("%y%m%d-%H%M")
    export_list = []

    # import files
    #run('/home/pi3ce/03_DevProjects/carezza_dev/carezza-design/import_assist/lib/download_box_file.sh')
    run('/cron_import/static/sh/download_box_file.sh')
    
    # get filename(s)
    proc_pos = False
    for file_path in Path(args.input).glob(f'{po_suffix}*.csv'):
        print(f'path: {file_path.parent} | file: {file_path.name}')
        success = convert_po.convert_data(str(file_path), output_folder=args.output, encoding=args.encoding,
                                      delimiter=args.delimiter, local_time=args.time)
        if success:
    #     # if True:
            run(f'{args.output}purchase_order.sh')
            proc_pos = True
            f_input = Path(f'{args.input}{file_path.name}')
            f_output = Path(f'{args.input}{processed_dir}{timestamp}-{file_path.stem}.csv')
            print(f'input: {f_input} | output: {f_output}')
        #     # move(f_input, f_output)
            export_list.append(f_output)

    # for file_path in Path(args.input).glob(f'{receipts_suffix}*.csv'):
    #     print(f'path: {file_path.parent} | file: {file_path.name}')
    #     success = convert_receipts.convert_data(str(file_path), output_folder=args.output, encoding=args.encoding,
    #                                   delimiter=args.delimiter, local_time=args.time)
    #     if success:
    #     # if True:
    #         run(f'{args.output}purchase_order_receipts.sh')
    #         # proc_receipts = True
    #         proc_pos = True
    #         f_input = Path(f'{args.input}{file_path.name}')
    #         f_output = Path(f'{args.input}{processed_dir}{timestamp}-{file_path.stem}.csv')
    #         print(f'input: {f_input} | output: {f_output}')
    #         move(f_input, f_output)
    #     #     export_list.append(f_output)

    # if proc_pos or proc_receipts:
    # if proc_pos:
    #     processor = process_records.OdooProcessor()
    #     processor.process_pos()
        # if proc_receipts:
        #     processor.process_receipts()


    print('checking proc process: %s', proc_pos)
    # if True:
    if proc_pos:
        print('Processing pos')
        try:
            processor = OdooProcessor()
            processor.process_pos()
        except Exception as e:
            print(f"Failed to process PO's: {e}")
    #     print('closing pos')
        # run(f'{args.output}purchase_order_status_done.sh')
        run('/cron_import/static/sh/move_logs.sh')

    print(export_list)
    print("--== FINISHED ==--")



    # upload files.
        # print(success)
    # print(listdir(args.input))
    # po_file =
    # import_file = 'a'
    # print(import_file)

def proc_recs():
        processor = OdooProcessor()
        # processor.process_receipts()
        processor.process_pos()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import CSV file')
    # parser.add_argument('-c', '--config', dest='config', default="conf/connection.conf", help='Configuration File that contains connection parameters', required = True)

    parser.add_argument('-i', '--input_folder', dest='input', help='Folder location for input files', default='./')
    # parser.add_argument('-f', '--file', dest='filename', help='File to import', required=True)
    parser.add_argument('-o', '--output_folder', dest='output', help='Folder location for output files', default='./')
    parser.add_argument('-e', '--encoding', dest='encoding', help='Encoding format of file', default='UTF-8')
    parser.add_argument('-d', '--delimiter', dest='delimiter', help='Delimiter used in CSV', default=',')
    parser.add_argument('-t', '--time_offset', dest='time', help='Local time to use', default='08:00:00')

    args = parser.parse_args()

    # print(f'Input: {args.input_location}{args.filename} | output: {args.output_location}')
    print(f'Input: {args.input} | output: {args.output}')

    run_stack()
    # proc_recs()
# print(args.filename)
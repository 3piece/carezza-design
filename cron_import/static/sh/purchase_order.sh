#! /bin/bash
#module_path="/home/pi3ce/00_x_to_Sync/11_gitlab/carezza/carezza-design/cron_import"
module_path="/home/odoo/src/user/cron_import/"
#import_path='/home/pi3ce/03_DevProjects/carezza_dev/import_files/'
conf_path=${module_path}'static/conf/'
import_path="/home/odoo/imports/"
working_path=${import_path}'origin/working/'
odoo_csv_import_module="/home/odoo/src/user/tfrancoi/odoo_csv_import/"

python3 ${odoo_csv_import_module}odoo_import_thread.py -c ${conf_path}connection.conf --file=${working_path}purchase.order.csv --model=purchase.order --encoding=utf-8 --worker=1 --size=20 --groupby= --ignore="status_switch" --sep=";" --context="{'tracking_disable': True}" > ${working_path}po_error.log 2>&1
python3 ${odoo_csv_import_module}odoo_import_thread.py -c ${conf_path}connection.conf --fail --file=${working_path}purchase.order.csv --model=purchase.order --encoding=utf-8 --ignore= --sep=";" --ignore= --context="{'tracking_disable': True}"

python3 ${odoo_csv_import_module}odoo_import_thread.py -c ${conf_path}connection.conf --file=${working_path}purchase.order.lines.csv --model=purchase.order.line --encoding=utf-8 --worker=1 --size=20 --groupby= --ignore="status_switch" --sep=";" --context="{'tracking_disable': True}" > ${working_path}po_lines_error.log 2>&1
python3 ${odoo_csv_import_module}odoo_import_thread.py -c ${conf_path}connection.conf --fail --file=${working_path}purchase.order.lines.csv --model=purchase.order.line --encoding=utf-8 --ignore= --sep=";" --context="{'tracking_disable': True}"
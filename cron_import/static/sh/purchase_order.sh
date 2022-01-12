#! /bin/bash
module_path="/home/odoo/src/user/cron_import/"
conf_path=${module_path}'static/conf/'
import_path="/home/odoo/imports/"
working_path=${import_path}'origin/working/'

/usr/bin/python3.9 -m odoo_import_thread -c ${conf_path}connection.conf --file=${working_path}purchase.order.csv --model=purchase.order --encoding=utf-8 --worker=1 --size=20 --groupby= --ignore="status_switch" --sep=";" --context="{'tracking_disable': True}" > ${working_path}po_error.log 2>&1
/usr/bin/python3.9 -m odoo_import_thread -c ${conf_path}connection.conf --fail --file=${working_path}purchase.order.csv --model=purchase.order --encoding=utf-8 --ignore= --sep=";" --ignore= --context="{'tracking_disable': True}"

/usr/bin/python3.9 -m odoo_import_thread -c ${conf_path}connection.conf --file=${working_path}purchase.order.lines.csv --model=purchase.order.line --encoding=utf-8 --worker=1 --size=20 --groupby= --ignore="status_switch" --sep=";" --context="{'tracking_disable': True}" > ${working_path}po_lines_error.log 2>&1
/usr/bin/python3.9 -m odoo_import_thread -c ${conf_path}connection.conf --fail --file=${working_path}purchase.order.lines.csv --model=purchase.order.line --encoding=utf-8 --ignore= --sep=";" --context="{'tracking_disable': True}"
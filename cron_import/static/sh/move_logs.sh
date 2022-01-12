#! /bin/bash
import_path="/home/odoo/imports/"
working_path=${import_path}'origin/working/'
processed_path=${import_path}'origin/source_files/processed/'
export_path=${import_path}'origin/exports/'

timestamp=$(date +'%y%m%d-%H%M')
ts_hour=$(date +'%y%m%d-%H')

mkdir ${export_path}${timestamp}
mv ${working_path}*.log ${export_path}${timestamp}/
mv ${working_path}*.bis ${export_path}${timestamp}/
mv ${processed_path}${ts_hour}* ${export_path}${timestamp}/
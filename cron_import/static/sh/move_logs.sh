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
cp ${processed_path}${ts_hour}* ${export_path}${timestamp}/

#mv f'/home/odoo/imports/origin/working/*.log' '/home/odoo/imports/origin/exports/ts/'
#mv f'/home/odoo/imports/origin/working/*.bis' '/home/odoo/imports/origin/exports/ts/'
#cp '/home/odoo/imports/origin/source_files/processed/ts/' '/home/odoo/imports/origin/exports/ts/'
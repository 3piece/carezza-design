#! /bin/bash

timestamp=$(date +'%y%m%d-%H%M')
mkdir /home/pi3ce/03_DevProjects/carezza_dev/carezza-design/import_assist/output_3/*.log /home/pi3ce/03_DevProjects/carezza_dev/carezza-design/import_assist/o_logs_out/${timestamp}
mv /home/pi3ce/03_DevProjects/carezza_dev/carezza-design/import_assist/output_3/*.log /home/pi3ce/03_DevProjects/carezza_dev/carezza-design/import_assist/o_logs_out/${timestamp}/
mv /home/pi3ce/03_DevProjects/carezza_dev/carezza-design/import_assist/output_3/*.bis /home/pi3ce/03_DevProjects/carezza_dev/carezza-design/import_assist/o_logs_out/${timestamp}/
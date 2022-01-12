#! /bin/bash

#  TODO: Check box for a. latest version and compare to local log.
#  TODO: Create a local log file, probably CSV format as follows (or key/value)
#  CSV file header :  version_no, md5_hash, timestamp
#  TODO: Upgrade to python box api.

box_prefix='https://app.box.com/shared/static/'
#filepoint='fsfjh4mcp81qsiby5c19mfym4npt1597'
filepoint_receipt='xkepsq6cixu3f934ltvbprsxexrl4k7o'  # Receipt
filepoint_po='drvyqoce396m39eqj2nhhqdcpxq9fuz6'  # PO
#https://app.box.com/s/drvyqoce396m39eqj2nhhqdcpxq9fuz6  # Odoo 1.1 PO only. MPO_APO Data_Import (65&co.).csv
#https://app.box.com/s/xkepsq6cixu3f934ltvbprsxexrl4k7o # Odoo 1.2 PO Receipt. MPO_APO Data_Import (65&co.).csv
timestamp=$(date +'%y%m%d-%H%M')
root_path="/home/pi3ce/03_DevProjects/carezza_dev/carezza-design/import_assist/"
output_path=${root_path}'origin/source_files/'
proc_path=${output_path}'processed/'
po_file='po'
receipt_file='rcpt'
file_type='csv'
temp_file='.tmpfile'

# echo $box_prefix$filepoint
#echo ${output_path}${po_file}_${timestamp}.${file_type}
for box_file in ${filepoint_po} ${filepoint_receipt}
do
  echo "Box File | ${box_prefix}${box_file}"
  curl -L ${box_prefix}${box_file} --output ${output_path}${temp_file}
  filesha=($(sha1sum ${output_path}${temp_file}))
  #echo "FileSha | ${filesha}"

  if compgen -G "${output_path}*${filesha}*" > /dev/null || compgen -G "${proc_path}*${filesha}*" > /dev/null ; then
#  if compgen -G "${proc_path}*${filesha}*" > /dev/null; then
      rm ${output_path}${temp_file}
      echo "${proc_path}${filesha} exists."
  else
  #    echo "FileSha | ${filesha}"
  #    echo "Source | ${output_path}${temp_file}"
  #    echo "Target | ${output_path}${filesha}-${po_file}"
      echo "File equailty | ${box_file} = ${filepoint_receipt}"
      file_name=${po_file}
      if [[ ${box_file} == ${filepoint_receipt} ]]
      then
        echo "equal"
        file_name=${receipt_file}
      else
        echo "not equal"
      fi
      mv -T ${output_path}${temp_file} ${output_path}${file_name}-${filesha}.${file_type}
      echo "${filesha} created."
  fi
done

#echo ${filesha}
#curl -L ${box_prefix}${filepoint_po} --output ${output_path}${po_file}_${timestamp}.${file_type}
#curl -L ${box_prefix}${filepoint_receipt} --output ${output_path}${receipt_file}_${timestamp}.${file_type}
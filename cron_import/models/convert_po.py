# -*- coding: utf-8 -*-
from odoo.addons.odoo_csv_tools.lib import mapper
from odoo.addons.odoo_csv_tools.lib.transform import Processor
from .prefix import *
from re import sub as re_sub

# Custom import
from datetime import datetime   # used to change the format of datetime fields

#  References
#  https://github.com/tfrancoi/odoo_csv_import#import-parameters
#  https://github.com/tfrancoi/odoo_import_example


# PURCHASE_ORDER_PREFIX
# PURCHASE_ORDER_LINE_PREFIX
# PURCHASE_ORDER_DELIVERY_PREFIX

# def get_po_number_n_type(po_number):
#     """ Formats an MPO number from 'MPO21/03/000126' to '2103-0126' also returning the type, either MPO or APO"""
#     po_type = po_number[0:3]
#     po_year = po_number[3:5]
#     po_month = po_number[6:8]
#     po_number = po_number[11:15]
#     return po_type, '{}{}-{}'.format(po_year, po_month, po_number)

#  "Supplier","MPO/APO No.","PO Date","Delivery Date (PO)","Code/Item","Color","Material Type","PO Qty","Purchase Currency","unit  (Orig. Currency)","Status  (PO)","Resp. By  (PO)","Payment Terms  (PO)","Inco Term  (PO)","Remarks  (PO)","Material Remarks",
#
# LOC_IN = '../origin/source_files/'
# FILE_IN = 'a1b1f41834efddc1a516bb2d92e8293e01f34430-po.csv'
#
# LOC_OUT = '../output_3/'
# # ENCODING = 'iso-8859-1'
# ENCODING = 'UTF-8'
# GMT_TIME = '08:00:00'

# state_map = {
#     'new': 'draft',
#     'confirmed': 'to approve',
#     'completed': 'done'
# }


state_map = {
    'new': 'draft',
    'confirmed': 'sent',
    'completed': 'done'
}

# Alvin notes all names will be updated into Odoo to align with Aspiring.
# user_map = {
#     '': '',
#     '': ''
# }

# 'new': 'Draft',
# 'confirmed': 'To Approve',
# 'completed': 'Locked'

def format_po_number(po_number):
    """ Receives an MPO number: 'MPO21/03/000126', returns a '2103-0126'

    Args:
        po_number (string): The MPO/APO number exported by Aspiring: 'MPO21/03/000126'

    Returns:
         formatted_po_number (string): number formatted as TypeChar-YYMM-PO_num, i.e.: 'M-2103-0126'
    """
    # po_type_char = po_number[0:1]
    po_year = po_number[3:5]
    po_month = po_number[6:8]
    po_number = po_number[11:15]
    # return '{}-{}{}-{}'.format(po_type_char, po_year, po_month, po_number)
    return '{}{}-{}'.format(po_year, po_month, po_number)


# def get_po_type(po_number):
#     """ Receives an MPO number: 'MPO21/03/000126', returning the type, either MPO or APO
#
#     Args:
#         po_number (string): The MPO/APO number exported by Aspiring: 'MPO21/03/000126'
#
#     Returns:
#          po_type (string): Either MPO or APO (the first 3 chars)
#     """
#     return po_number[0:3]


# def my_preprocessor(header, data):
#     header.append('PO_Type')
#     header.append('PO_Number')
#     for i, j in enumerate(data):
#         line = dict(zip(header, j))
#         po_type, po_number = get_po_number_n_type(line['MPO/APO No.'])
#         data[i].append(po_type)
#         data[i].append(po_number)
#     return header, data

def delivery_preprocessor(header, data):
    data_new = []
    for i, j in enumerate(data):
        line = dict(zip(header, j))
        if line['Received Qty']:  # and len()>1
            data_new.append(j)
    return header, data_new


def convert_data(import_file, output_folder='./', encoding='UTF-8', delimiter=',', local_time='08:00:00'):
    """
        Convert data from input CSV to ouput CSV through mappings

    :param import_file:
    :param output_folder:
    :param encoding:
    :param delimiter:
    :param local_time:
    :return:
    """

    # encoding = 'iso-8859-1'
    print(f'file: {import_file} | delimiter: {delimiter} | enc: {encoding}')

    processor = Processor(import_file, delimiter=',', encoding=encoding)
    # deliver_processor = Processor('../origin/odoo_po_import_19.csv', delimiter=',', preprocess=delivery_preprocessor, encoding='iso-8859-1')
        # conf_file='/home/pi3ce/03_DevProjects/carezza/odoo14_carezza_staging.conf'

    # vendor_partner_mapping = {
    #     'id': mapper.m2o_map(PURCHASE_VENDOR_PARTNER_PREFIX, mapper.val(
    #         'Supplier',
    #         postprocess=lambda x: re_sub(r"[^a-zA-Z0-9_-]+", "", x.strip().replace(" ", "_")))),
    #     'name': mapper.val('Supplier')
    # }

# Show date_order as "PO date"
    # Vendor performance: Receipt date - PO date

    purchase_order_mapping = {
        #  "id";"origin";"name";"partner_id/id";"currency_id";"date_order";"date_approve";"payment_term_id";"incoterm_id";"state"
        'id': mapper.m2o_map(PURCHASE_ORDER_PREFIX, mapper.val('MPO/APO No.', postprocess=lambda x: format_po_number(x))),
        # 'id': mapper.m2o(PURCHASE_ORDER_PREFIX, 'MPO/APO No.'),
        'origin': mapper.val('MPO/APO No.'),
        'name': mapper.val('MPO/APO No.', postprocess=lambda x: format_po_number(x)),
        'partner_id/id': mapper.m2o_map(PURCHASE_VENDOR_PARTNER_PREFIX, mapper.val(
            'Supplier',
            postprocess=lambda x: PURCHASE_VENDOR_NAME_PREFIX + re_sub(r"[^a-zA-Z0-9_-]+", "", x.strip().replace(" ", "_")))),
        # 'po_type': mapper.val('MPO/APO No.', postprocess=lambda x: get_po_type(x)),
        # 'name': mapper.concat(' ','Firstname','Lastname'),
        'currency_id': mapper.val('Purchase Currency'),
        'date_order': mapper.val('PO Date', postprocess=lambda x: datetime.strptime(x, "%d/%b/%Y").strftime("%Y-%m-%d " + local_time)),
        # 'date_approve': mapper.val('PO Date', postprocess=lambda x: datetime.strptime(x, "%d/%b/%Y").strftime("%Y-%m-%d " + local_time)),
        # 'date_planned': mapper.val('Delivery Date (PO)', postprocess=lambda x: datetime.strptime(x, "%d/%b/%Y").strftime("%Y-%m-%d " + GMT_TIME) if x else ''),
        'payment_term_id': mapper.val('Payment Terms  (PO)'),
        'incoterm_id': mapper.val('Inco Term  (PO)'),
        'state': mapper.map_val('Status  (PO)', state_map),
        'notes': mapper.val('Remarks  (PO)'),
        'user_id': mapper.val('Resp. By  (PO)'),
        'po_date': mapper.val('PO Date', postprocess=lambda x: datetime.strptime(x, "%d/%b/%Y").strftime("%Y-%m-%d " + local_time)),
        'status_switch': mapper.val('Status  (PO)')
    }

    purchase_order_lines_mapping = {
        #  "id";"order_id";"product_id/id";"name";"product_qty";"price_unit"
        'id': mapper.m2o_map(PURCHASE_ORDER_LINE_PREFIX, mapper.concat_mapper_all(
            '-',
            mapper.val('MPO/APO No.', postprocess=lambda x: format_po_number(x)),
            mapper.val('Code/Item', postprocess=lambda x: re_sub(r"[^a-zA-Z0-9_-]+", "", x.strip().replace(" ", "_"))),
            mapper.val('Color', postprocess=lambda x: re_sub(r"[^a-zA-Z0-9_-]+", "", x.strip().replace(" ", "_"))))),
        'order_id': mapper.val('MPO/APO No.', postprocess=lambda x: format_po_number(x)),
        'product_id/id': mapper.m2o_map(PRODUCT_PRODUCT_MATERIAL_PREFIX, mapper.concat_mapper_all(
            '_',
            # mapper.val('Code/Item', postprocess=lambda x: re_sub(r"[^a-zA-Z0-9_-]+", "", x.strip().replace(" ", "_"))),
            # mapper.val('Color', postprocess=lambda x: re_sub(r"[^a-zA-Z0-9_-]+", "", x.strip().replace(" ", "_"))))),
            mapper.val('Code/Item', postprocess=lambda x: x.strip().replace('(', '').replace(')', '').replace(" ", "_").replace('.', '_')),
            mapper.val('Color', postprocess=lambda x: x.strip().replace('(', '').replace(')', '').replace(" ", "_").replace('.', '_')))),
        'name': mapper.concat_mapper_all(
            '-',
            mapper.val('Code/Item', postprocess=lambda x: re_sub(r"[^ a-zA-Z0-9_-]+", "", x.strip())),
            mapper.val('Color', postprocess=lambda x: re_sub(r"[^ a-zA-Z0-9_-]+", "", x.strip()))),
        # 'date_order': mapper.val('PO Date', postprocess=lambda x: datetime.strptime(x, "%d/%b/%Y").strftime("%Y-%m-%d " + GMT_TIME)),
        # 'date_planned': mapper.val_fallback('Delivery Date (PO)', 'PO Date', postprocess=lambda x: datetime.strptime(x, "%d/%b/%Y").strftime("%Y-%m-%d " + GMT_TIME) if x else ''),
        'product_qty': mapper.val('PO Qty'),
        # 'price_unit': mapper.val('Purchase Price  (Orig. Currency)'),
        'price_unit': mapper.val('unit  (Orig. Currency)'),
        # 'move_dest_ids':
    }

    # purchase_order_stock_picking_mapping = {
    #     'id': mapper.m2o_map(PURCHASE_ORDER_STOCK_PICKING_PREFIX, mapper.concat_mapper_all('-',
    #         mapper.val('MPO/APO No.', postprocess=lambda x: format_po_number(x)),
    #         mapper.val('Date (Material Receive)', postprocess=lambda x: datetime.strptime(x, "%d/%b/%Y").strftime("%y%m%d")))),
    #     'partner_id/id': mapper.m2o_map(PURCHASE_VENDOR_PARTNER_PREFIX, mapper.val(
    #         'Supplier',
    #         postprocess=lambda x: re_sub(r"[^a-zA-Z0-9_-]+", "", x.strip().replace(" ", "_")))),
    #     'picking_type_id': mapper.const('Receipts'),
    #     'location_id': mapper.const('Partner Locations/Vendors'),
    #     'location_dest_id': mapper.const('WH/Stock'),
    #     'scheduled_date': mapper.val('Date (Material Receive)', postprocess=lambda x: datetime.strptime(x, "%d/%b/%Y").strftime("%Y-%m-%d 00:00:00")),
    #     'origin': mapper.val('MPO/APO No.', postprocess=lambda x: format_po_number(x)),
    #     # 'state': mapper.const('done'),
    # }
    #
    # purchase_order_stock_move_mapping = {
    #     'id': mapper.m2o_map(PURCHASE_ORDER_STOCK_MOVE_PREFIX, mapper.concat_mapper_all(
    #         '-',
    #         mapper.val('MPO/APO No.', postprocess=lambda x: format_po_number(x)),
    #         mapper.val('Date (Material Receive)', postprocess=lambda x: datetime.strptime(x, "%d/%b/%Y").strftime("%y%m%d")),
    #         mapper.val('Code/Item', postprocess=lambda x: re_sub(r"[^a-zA-Z0-9_-]+", "", x.strip().replace(" ", "_"))),
    #         mapper.val('Color', postprocess=lambda x: re_sub(r"[^a-zA-Z0-9_-]+", "", x.strip().replace(" ", "_"))))),
    #     'picking_id/id': mapper.m2o_map(PURCHASE_ORDER_STOCK_PICKING_PREFIX, mapper.concat_mapper_all(
    #         '-',
    #         mapper.val('MPO/APO No.', postprocess=lambda x: format_po_number(x)),
    #         mapper.val('Date (Material Receive)', postprocess=lambda x: datetime.strptime(x, "%d/%b/%Y").strftime("%y%m%d")))),
    #     'product_id/id': mapper.m2o_map(PRODUCT_PRODUCT_MATERIAL_PREFIX, mapper.concat_mapper_all(
    #         '_',
    #         mapper.val('Code/Item', postprocess=lambda x: re_sub(r"[^a-zA-Z0-9_-]+", "", x.strip().replace(" ", "_"))),
    #         mapper.val('Color', postprocess=lambda x: re_sub(r"[^a-zA-Z0-9_-]+", "", x.strip().replace(" ", "_"))))),
    #     # 'product_id': mapper.concat_mapper_all(
    #     #     '-',
    #     #     mapper.val('Code/Item', postprocess=lambda x: re_sub(r"[^ a-zA-Z0-9_-]+", "", x.strip())),
    #     #     mapper.val('Color', postprocess=lambda x: re_sub(r"[^ a-zA-Z0-9_-]+", "", x.strip()))),
    #     'product_uom_qty': mapper.val('Received Qty'),
    #     'quantity_done': mapper.val('Received Qty'),
    #     'name': mapper.const('Imported from Aspiring'),
    #     'product_uom': mapper.const('M'),
    #     'location_id': mapper.const('Partner Locations/Vendors'),
    #     'location_dest_id': mapper.const('WH/Stock'),
    # }


    # processor.process(vendor_partner_mapping, './output/vendor.res.partner.csv', {'model': 'res.partner', 'context': "{'tracking_disable': True}", 'worker': 1, 'batch_size': 20}, 'set')
    print('Processing: Purchase Order Mapping')
    processor.process(purchase_order_mapping, output_folder + 'purchase.order.csv', {'model': 'purchase.order', 'context': "{'tracking_disable': True}", 'worker': 1, 'batch_size': 20}, 'set')
    print('Processing: Purchase Order Lines Mapping')
    processor.process(purchase_order_lines_mapping, output_folder + 'purchase.order.lines.csv', {'model': 'purchase.order.line', 'context': "{'tracking_disable': True}", 'worker': 1, 'batch_size': 20}, 'set')
    # deliver_processor.process(purchase_order_stock_picking_mapping, '../output/purchase.order.stock.picking.csv', {'model': 'stock.picking', 'context': "{'tracking_disable': True}", 'worker': 1, 'batch_size': 20}, 'set')
    # deliver_processor.process(purchase_order_stock_move_mapping, '../output/purchase.order.stock.move.csv', {'model': 'stock.move', 'context': "{'tracking_disable': True}", 'worker': 1, 'batch_size': 20}, 'set')
    print('Processing: Write to File')
    processor.write_to_file(output_folder + 'purchase_order_2.sh', python_exe='', path='../')  # Using static file, \
    #    can re-enable this, need to add ignore for swtich_case
    # deliver_processor.write_to_file("../output/purchase_order_stock_move.sh", python_exe='', path='')
    return True

# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError
import pandas as pd
import base64
import io
import csv

class StockPicking(models.Model):

    _inherit = 'stock.picking'

    ship_date = fields.Date(string="Ship Date")
    bl_number = fields.Char(string='B/L Number')
    is_propagation = fields.Boolean(related='picking_type_id.is_propagation')
    po_date = fields.Date(related='purchase_id.po_date')
    is_locked = fields.Boolean(default=False, help='When the picking is not done this allows changing the '
                               'initial demand. When the picking is done this allows '
                               'changing the done quantities.')
    excel_template = fields.Binary()
    excel_template_name = fields.Char("Filename")
    upload_excel_file = fields.Binary()
    upload_excel_name = fields.Char("Filename")
#     @api.model
#     def create(self, vals):
#         res = super().create(vals)
#         if res.po_date:
#             ship_date = res.po_date +  datetime.timedelta(days=14)
#             res.ship_date = ship_date
#         return res
#


    def button_validate(self):
        res = super().button_validate()
        for move_line_id in self.move_line_ids_without_package:
            if move_line_id.lot_id:
                move_line_id.lot_id.pallet_number = move_line_id.pallet_number
                move_line_id.lot_id.hides = move_line_id.hides
        return res

    @api.onchange('move_ids_without_package')
    def onchange_move_ids_without_package(self):
        if self.is_propagation:
            procurement_group = self.env['procurement.group'].search(
                [('picking_id', '=', self.id)])
            for stock_move in self.move_ids_without_package:
                if stock_move.group_id:
                    procurement_group = stock_move.group_id

            if not procurement_group:
                if self.move_ids_without_package:
                    procurement_group_name = self.env['ir.sequence'].next_by_code(
                        'procurement.group')
                    procurement_group = self.env['procurement.group'].create({'name': procurement_group_name,
                                                                              'move_type': 'direct'})
            for stock_move in self.move_ids_without_package:
                stock_move.group_id = procurement_group.id


    def update_exist_transfer(self,transfer,details):
        for move in transfer.move_ids_without_package:
            for detail in details:
                # Update move_line base on line_id
                if detail['move_line_id']:
                    move_line = self.env['stock.move.line'].search([('picking_id','=',transfer.id),('id','=',detail['move_line_id'])])
                    if move_line:
                        move_line.qty_done = detail['qty_done']
                        move_line.pallet_number = detail['pallet_number']
                        move_line.hides = detail['hides']
                
                #Create new move line
                if move.product_id.id == detail['product_id']:
                    vals= {'product_id' : move.product_id.id,
                           'picking_id': transfer.id,
                           'move_id': move.id,
                           'product_uom_id': move.product_id.uom_id.id,
                           'qty_done': detail['qty_done'],
                           'location_id': transfer.location_id.id,
                           'location_dest_id': transfer.location_dest_id.id,
                           'state': 'assigned',
                           'pallet_number': detail['pallet_number'],
                           'hides': detail['hides']
                           }
                    move_line = self.env['stock.move.line'].create(vals)
                    

    def check_transfer(self, details):
        # TODO:  will have logic check all line must have the same
        # purchase_name
        for detail in details:
            transfer = self.env['stock.picking'].search(
                [('name', '=', detail['picking_name']), ('state', '=', 'assigned')])
            self.update_exist_transfer(transfer, details)          
    
    def read_csv(self,upload_excel_file):
        list_obj = []
        csv_data = base64.b64decode(upload_excel_file)
        data_file = io.StringIO(csv_data.decode("utf-8"))
        data_file.seek(0)
        file_reader = []
        csv_reader = csv.reader(data_file, delimiter=',')
        file_reader.extend(csv_reader)
        header = True
        list_move_line_id = []
        for obj in file_reader:
            if header:
                header = False
            else:
                dict_val = {
                'ship_date': obj[0],
                'picking_name' : obj[1],
                'product_name': obj[2],
                'product_id': int(obj[3]),
                'qty_done': obj[4],
                'pallet_number': obj[5],
                'hides': obj[6],
                'move_line_id': int(obj[7]) if obj[7] != '' else False }
                list_obj.append(dict_val)
                if obj[7] != '':
                    list_move_line_id.append(int(object))
        return list_obj
                    
    def write(self, vals):
        res = super().write(vals)
        if 'ship_date' in vals:
            for stock_move_line in record.move_line_ids_without_package:
                ship_date = record.ship_date
                stock_move_line.lot_id.ship_date = ship_date 
                       
        if 'upload_excel_file' in vals:
            if vals['upload_excel_file']: 
                list_obj = self.read_csv(self.upload_excel_file)        
                self.check_transfer(list_obj)
        return res


                    #move._action_confirm()
                    #move._action_done()
#
#

#
#
#
#     def test_details_insert(self):
#         details = [{
#                     'picking_name' : 'UnI/UNI-Cust-TTF/00351',
#                     'product_name': "LG-1310-C",
#                     'product_id': 824,
#                     'demand_qty': 1,
#                     'pallet_number': 1,
#                     'hides': 10,
#                     'crud' : 'update'}]
#         self.check_transfer(details)
#
#     def create_new_transfer(self,details=None):
#         details = [{
#                     'picking_name' : 'UnI/UNI-Cust-TTF/00351',
#                     'product_name': "LG-1310-C",
#                     'product_id': 824,
#                     'demand_qty': 1,
#                     'pallet_number': 1,
#                     'hides': 10,
#                     'crud' : 'update'}]
#
    def process(self):
        pickings_to_do = self.env['stock.picking']
        pickings_not_to_do = self.env['stock.picking']
        for line in self.backorder_confirmation_line_ids:
            if line.to_backorder is True:
                pickings_to_do |= line.picking_id
            else:
                pickings_not_to_do |= line.picking_id

        for pick_id in pickings_not_to_do:
            moves_to_log = {}
            for move in pick_id.move_lines:
                if float_compare(move.product_uom_qty,
                                 move.quantity_done,
                                 precision_rounding=move.product_uom.rounding) > 0:
                    moves_to_log[move] = (move.quantity_done, move.product_uom_qty)
            pick_id._log_less_quantities_than_expected(moves_to_log)

        pickings_to_validate = self.env.context.get('button_validate_picking_ids')
        if pickings_to_validate:
            pickings_to_validate = self.env['stock.picking'].browse(pickings_to_validate).with_context(skip_backorder=True)
            if pickings_not_to_do:
                pickings_to_validate = pickings_to_validate.with_context(picking_ids_not_to_backorder=pickings_not_to_do.ids)
            return pickings_to_validate.button_validate()
        return True

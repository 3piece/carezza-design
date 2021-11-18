# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    ship_date =  fields.Date(string="Ship Date")
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
    def write(self,vals):
        for record in self:
            res = super().write(vals)
            if 'ship_date' in vals:
                for stock_move_line in record.move_line_ids_without_package:
                    ship_date = record.ship_date
                    stock_move_line.lot_id.ship_date = ship_date
            return res   
   
    
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
            procurement_group = self.env['procurement.group'].search([('picking_id','=',self.id)])
            for stock_move in self.move_ids_without_package:
                if stock_move.group_id:
                    procurement_group = stock_move.group_id
            
            if not procurement_group:
                if self.move_ids_without_package:
                    procurement_group_name = self.env['ir.sequence'].next_by_code('procurement.group')
                    procurement_group = self.env['procurement.group'].create({'name': procurement_group_name,
                                                                              'move_type': 'direct'})
            for stock_move in self.move_ids_without_package:
                stock_move.group_id = procurement_group.id
            
            
#     def update_exist_transfer(self,transfer,details):
#         for move in transfer.move_ids_without_package:
#             for detail in details:
#                 if move.product_id.id == int(detail['product_id']):
#                     vals= {'product_id' : move.product_id.id,
#                            'picking_id': transfer.id,
#                            'move_id': move.id,
#                            'product_uom_id': move.product_id.uom_id.id,
#                            'demand_qty': detail['demand_qty'],
#                            'location_id': transfer.location_id.id,
#                            'location_dest_id': transfer.location_dest_id.id,
#                            'state': 'assigned',
#                            'pallet_number': detail['pallet_number'],
#                            'hides': detail['hides']}
#                     move_line = self.env['stock.move.line'].create(vals)
#                     #move._action_confirm()
#                     #move._action_done()
#                     
# 
#     def check_transfer(self ,details):  
#         # TODO:  will have logic check all line must have the same purchase_name
#         transfer = self.env['stock.picking'].search([('origin','=',details[0]['purchase_name']),('state','=','assigned')])
#         self.update_exist_transfer(transfer, details)
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
#     def process(self):
#         pickings_to_do = self.env['stock.picking']
#         pickings_not_to_do = self.env['stock.picking']
#         for line in self.backorder_confirmation_line_ids:
#             if line.to_backorder is True:
#                 pickings_to_do |= line.picking_id
#             else:
#                 pickings_not_to_do |= line.picking_id
# 
#         for pick_id in pickings_not_to_do:
#             moves_to_log = {}
#             for move in pick_id.move_lines:
#                 if float_compare(move.product_uom_qty,
#                                  move.quantity_done,
#                                  precision_rounding=move.product_uom.rounding) > 0:
#                     moves_to_log[move] = (move.quantity_done, move.product_uom_qty)
#             pick_id._log_less_quantities_than_expected(moves_to_log)
# 
#         pickings_to_validate = self.env.context.get('button_validate_picking_ids')
#         if pickings_to_validate:
#             pickings_to_validate = self.env['stock.picking'].browse(pickings_to_validate).with_context(skip_backorder=True)
#             if pickings_not_to_do:
#                 pickings_to_validate = pickings_to_validate.with_context(picking_ids_not_to_backorder=pickings_not_to_do.ids)
#             return pickings_to_validate.button_validate()
#         return True                        

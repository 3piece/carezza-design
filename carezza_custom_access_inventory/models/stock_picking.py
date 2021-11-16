# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    ship_date =  fields.Date(string="Ship Date")
    bl_number = fields.Char(string='B/L Number')
    is_propagation = fields.Boolean(related='picking_type_id.is_propagation')
    po_date = fields.Date(related='purchase_id.po_date')
    
    @api.model
    def create(self, vals):
        res = super().create(vals)
        return res
   
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
            
            
                

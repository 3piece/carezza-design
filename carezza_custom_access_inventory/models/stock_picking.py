# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    eta =  fields.Date(string="ETA")
    bl_number = fields.Char(string='B/L Number')
    is_propagation = fields.Boolean(related='picking_type_id.is_propagation')
    
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
            
            
                

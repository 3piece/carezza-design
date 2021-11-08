# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockProductionLot(models.Model):

    _inherit = 'stock.production.lot'

    pallet_number = fields.Integer()
    hides = fields.Integer()
    po_id = fields.Many2one('purchase.order')
    supplier_id = fields.Many2one(related='po_id.partner_id')
    vendor_qty = fields.Float(compute='_compute_qty')
    
    #remove later
    number_of_skins = fields.Integer()
    
    def _compute_qty(self):
        for record in self:
            qty = 0
            move_lines = self.env['stock.move.line'].search([('lot_id','=',record.id)])
            for move_line in move_lines:
                qty+= move_line.qty_done
                record.vendor_qty = qty
    
    @api.model
    def create(self,vals):
        context = self.env.context
        if 'move_id' in context:
            move_id = self.env['stock.move'].browse([context['move_id']])
            if move_id:
                vals['po_id'] = move_id.purchase_line_id.order_id.id     
        res = super().create(vals)
        return res
    
    def write(self,vals):
        res = super().write(vals)
        return res
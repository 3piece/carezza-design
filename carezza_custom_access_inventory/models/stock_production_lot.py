# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockProductionLot(models.Model):

    _inherit = 'stock.production.lot'

    pallet_number = fields.Integer(string='Pallet / Box / Roll')
    hides = fields.Integer()
    po_id = fields.Many2one('purchase.order', string="PO")
    supplier_id = fields.Many2one('res.partner',related='po_id.partner_id')
    
    ship_date =  fields.Date(string="Ship Date")
    position = fields.Char('Position')
    #remove later
    number_of_skins = fields.Integer()

    supplier = fields.Char() #Added by Raymond
    material_desc = fields.Char() #Added by Raymond
    remark = fields.Char() #Added by Raymond
    coo = fields.Char() #Added by Raymond

#     def _compute_qty(self):
#         for record in self:
#             qty = 0
#             move_lines = self.env['stock.move.line'].search([('lot_id','=',record.id),('state','!=','cancel')])
#             for move_line in move_lines:
#                 qty+= move_line.demand_qty
#             record.vendor_qty = qty
    
    @api.model
    def create(self,vals):
        context = self.env.context
        if 'move_id' in context:
            move_id = self.env['stock.move'].browse([context['move_id']])
            if move_id:
                vals['po_id'] = move_id.purchase_line_id.order_id.id

                #Added by Raymond
                vals['supplier'] = move_id.supplier
                vals['remark'] = move_id.remark
                vals['material_desc'] = move_id.material_desc
                vals['coo'] = move_id.coo
                #===========================
        
        res = super().create(vals)
        return res
    
    def write(self,vals):
        res = super().write(vals)
        return res
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError
import datetime


class StockMove(models.Model):

    _inherit = 'stock.move'
    
    invoice_number =  fields.Char()
    invoice_date =  fields.Date()
    invoice_amount =  fields.Float()
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
        default=lambda self: self.env.company.currency_id.id)
    #average_skin_size = fields.Float(compute='compute_average_skin_size')
    average_skin_size = fields.Float()
#     def compute_average_skin_size(self):
#         for record in self:
#             result = 0
#             if record.hides  != 0:
#                 result = record.quantity_done/record.hides 
#             record.average_skin_size = result
    
    
    def create(self,vals):
        res = super().create(vals)
        if not res.picking_id.ship_date and res.picking_id.purchase_id:
            if res.picking_id.purchase_id.po_date:
                ship_date = res.picking_id.purchase_id.po_date +  datetime.timedelta(days=14)
                res.picking_id.ship_date = ship_date            
        return res
        

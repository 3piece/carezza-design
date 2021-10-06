# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockMove(models.Model):

    _inherit = 'stock.move'
    
    invoice_number =  fields.Char()
    invoice_date =  fields.Date()
    invoice_amount =  fields.Float()
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
        default=lambda self: self.env.company.currency_id.id)
    pallet_number = fields.Integer()
    number_of_skins = fields.Integer()
    average_skin_size = fields.Float(compute='compute_average_skin_size')
    
    def compute_average_skin_size(self):
        for record in self:
            result = 0
            if record.number_of_skins  != 0:
                result = record.quantity_done/record.number_of_skins 
            record.average_skin_size = result
    
    

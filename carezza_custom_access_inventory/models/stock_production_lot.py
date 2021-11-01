# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockProductionLot(models.Model):

    _inherit = 'stock.production.lot'

    pallet_number = fields.Integer()
    number_of_skins = fields.Integer()
    po_id = fields.Many2one('purchase.order')
    supplier_id = fields.Many2one('res.partner')
    
    @api.model
    def create(self,vals):
        res = super().create(vals)
        return res
    
    def write(self,vals):
        res = super().write(vals)
        return res
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockMoveLine(models.Model):

    _inherit = 'stock.move.line'
    
    pallet_number = fields.Integer(related='lot_id.pallet_number')
    number_of_skins = fields.Integer(related='lot_id.number_of_skins')


        
        
    
    
    

# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockMove(models.Model):

    _inherit = 'stock.move'
    
    invoice_number =  fields.Char()
    invoice_date =  fields.Date()
    invoice_mount =  fields.Float()
    

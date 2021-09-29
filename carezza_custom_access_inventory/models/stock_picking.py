# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    eta =  fields.Date(string="ETA")
    bl_number = fields.Char(string='B/L Number')
    

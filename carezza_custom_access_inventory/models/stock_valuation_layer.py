# -*- coding: utf-8 -*-
from odoo import models, fields, api, _



class stockValuationLayer(models.Model):

    _inherit = 'stock.valuation.layer'

    location_id  =  fields.Many2one(related='stock_move_id.location_id')
    location_dest_id  =  fields.Many2one(related='stock_move_id.location_dest_id')


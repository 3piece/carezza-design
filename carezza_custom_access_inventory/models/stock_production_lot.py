# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockProductionLot(models.Model):

    _inherit = 'stock.production.lot'

    pallet_number = fields.Integer()
    number_of_skins = fields.Integer()
    

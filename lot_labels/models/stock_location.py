# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockLocation(models.Model):

    _inherit = 'stock.location'

    responsible_user_ids = fields.Many2many('res.users')
    

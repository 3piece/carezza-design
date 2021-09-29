# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockWarehouse(models.Model):

    _inherit = 'stock.warehouse'

    responsible_user_ids = fields.Many2many('res.users')
    

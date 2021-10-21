# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockPickingType(models.Model):

    _inherit = 'stock.picking.type'

    responsible_user_ids = fields.Many2many('res.users')
    is_propagation = fields.Boolean()
    

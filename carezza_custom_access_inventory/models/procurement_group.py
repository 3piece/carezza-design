# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class ProcurementGroup(models.Model):

    _inherit = 'procurement.group'

    picking_id = fields.Many2one('stock.picking')
    

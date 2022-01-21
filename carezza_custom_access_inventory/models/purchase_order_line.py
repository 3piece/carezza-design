# -*- coding: utf-8 -*-

import logging
from odoo.exceptions import AccessError
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    default_code = fields.Char(related='product_id.default_code')
    attribute_value = fields.Char(related='product_id.attribute_value', string='Color')


        
    
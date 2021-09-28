# -*- coding: utf-8 -*-

from odoo.exceptions import AccessError
from odoo import models, fields, api, _

class ProductTemplate(models.Model):

    _inherit = 'product.template'

    default_code = fields.Char(
        'Code', compute='_compute_default_code',
        inverse='_set_default_code', store=True)
    
    
class ProductTemplate(models.Model):

    _inherit = 'product.product'

    default_code = fields.Char('Code', index=True)
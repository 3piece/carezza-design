# -*- coding: utf-8 -*-

import logging
from odoo.exceptions import AccessError, ValidationError
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    po_date = fields.Date(help="Date PO was created in Aspiring", String='PO Date')



    

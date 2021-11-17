# -*- coding: utf-8 -*-

import logging
from odoo.exceptions import AccessError
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    po_date = fields.Date(help="Date PO was created in Aspiring", String='PO Date')
    excel_template = fields.Binary()
    excel_template_name = fields.Char("Filename")
    upload_excel_file = fields.Binary()
    upload_excel_name = fields.Char("Filename")

        
    
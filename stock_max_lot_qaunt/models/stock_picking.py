# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

	def button_max_lot(self):
		_logger.info(f'Max Lot Quants - Maximizing..............')
		# Clean-up the context key at validation to avoid forcing the creation of immediate
		# transfers.
		# ctx = dict(self.env.context)
		# ctx.pop('default_immediate_transfer', None)

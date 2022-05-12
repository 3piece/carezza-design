# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_max_lots(self):
        for move_line in self.move_line_ids:
            if move_line.lot_id:
                max_qty = move_line.check_available_quantity(move_line.product_id, move_line.location_id, 1,
                                                                   move_line.lot_id)
                if max_qty > 0:
                    move_line.qty_done = max_qty
                    _logger.debug(f'Move Line: {move_line.id} | product: {move_line.product_id.name} | lot: {move_line.lot_id} | set qty_done : {max_qty}')
        _logger.info(f'Max Lot Quants - Maximizing..............')

#   TODO: Split code into 2 modules, 1 for stock, 1 for stock Barcode.
#   TODO: Review, clean-up and migrate check_available_quantity code to this stock module.
#    - hint: code follows Odoo method.


# Clean-up the context key at validation to avoid forcing the creation of immediate
# transfers.
# ctx = dict(self.env.context)
# ctx.pop('default_immediate_transfer', None)

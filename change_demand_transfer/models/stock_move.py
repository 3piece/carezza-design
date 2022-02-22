# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.onchange('product_uom_qty')
    def onchange_product_uom_qty(self):
        if self._origin.group_id:
            stock_moves = self.env['stock.move'].search([('group_id','=',self._origin.group_id.id),('product_id','=',self._origin.product_id.id)])
            for stock_move in stock_moves:
                stock_move.product_uom_qty = self.product_uom_qty
    
 
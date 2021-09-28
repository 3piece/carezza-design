# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockInventory(models.Model):

    _inherit = 'stock.inventory'

    def action_validate(self):
        if not self.user_has_groups('stock.group_stock_manager'):
              raise AccessError("You don't have permission")
        res = super().action_validate()
        return res



# -*- coding: utf-8 -*-

from odoo.exceptions import AccessError
from odoo import models, fields, api, _

class StockInventoryLine(models.Model):

    _inherit = 'stock.inventory.line'


    @api.model
    def create(self, vals):
        a = self.user_has_groups('carezza_custom_access_inventory.carezza_group_stock_checker')
        if not self.user_has_groups('carezza_custom_access_inventory.carezza_group_stock_checker'):
              raise AccessError("You don't have permission")
        res = super().create(vals)
        return res

    def write(self, vals):
        if not self.user_has_groups('carezza_custom_access_inventory.carezza_group_stock_checker'):
              raise AccessError("You don't have permission")
        res = super().write(vals)
        return res
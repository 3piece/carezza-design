# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockQuant(models.Model):

    _inherit = 'stock.quant'

    @api.model
    def _get_quants_action(self, domain=None, extend=False):
        """ Returns an action to open quant view.
        Depending of the context (user have right to be inventory mode or not),
        the list view will be editable or readonly.

        :param domain: List for the domain, empty by default.
        :param extend: If True, enables form, graph and pivot views. False by default.
        """
        self._quant_tasks()
        ctx = dict(self.env.context or {})
        ctx.pop('group_by', None)
        action = {
            'name': _('Stock On Hand'),
            'view_type': 'tree',
            'view_mode': 'list,form',
            'res_model': 'stock.quant',
            'type': 'ir.actions.act_window',
            'context': ctx,
            'domain': domain or [],
            'help': """
                <p class="o_view_nocontent_empty_folder">No Stock On Hand</p>
                <p>This analysis gives you an overview of the current stock
                level of your products.</p>
                """
        }

        target_action = self.env.ref('stock.dashboard_open_quants', False)
        if target_action:
            action['id'] = target_action.id

        if self._is_inventory_mode():
            action['view_id'] = self.env.ref('stock.view_stock_quant_tree_editable').id
            form_view = self.env.ref('stock.view_stock_quant_form_editable').id
        else:
            action['view_id'] = self.env.ref('stock.view_stock_quant_tree').id
            form_view = self.env.ref('stock.view_stock_quant_form').id
        action.update({
            'views': [
                (action['view_id'], 'list'),
                (form_view, 'form'),
            ],
        })
        if extend:
            action.update({
                'view_mode': 'pivot,graph,tree,form',
                'views': [
                    (self.env.ref('stock.view_stock_quant_pivot').id, 'pivot'),
                    (self.env.ref('stock.stock_quant_view_graph').id, 'graph'),                    
                    (action['view_id'], 'list'),
                    (form_view, 'form'),
                ],
            })
        return action

# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError
from collections import OrderedDict, defaultdict
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class StockMoveLine(models.Model):

    _inherit = 'stock.move.line'
    
    pallet_number = fields.Integer(string='Pallet / Box / Roll')
    hides = fields.Integer()
    
    #row_csv_line_id = fields.Integer(help='use to update line baseon csv')
   
    @api.onchange('lot_id')
    def onchange_lot_id(self):
        self.pallet_number = self.lot_id.pallet_number
        self.hides = self.lot_id.hides
        
        context = self.env.context
        if 'default_picking_id' in context:
            picking_id = context['default_picking_id']
        move_id = self.env['stock.move'].search([('product_id','=',self.product_id.id),('picking_id','=',picking_id)])
        qty_need = move_id.product_uom_qty- move_id.reserved_availability
        quants = self.env['stock.quant']._gather(self.product_id,self.location_id,self.lot_id)
        available_quantity = self.check_available_quantity(self.product_id,self.location_id,qty_need,self.lot_id)
        
        if available_quantity:
            if available_quantity > qty_need:
                self.product_uom_qty = qty_need  
                quants.reserved_quantity+= qty_need  
            else:
                self.product_uom_qty = available_quantity  
                quants.reserved_quantity+= qty_need      

#         if self._origin.lot_id != self.lot_id:
#             quants = self.env['stock.quant']._gather(self.product_id,self.location_id,self._origin.lot_id)
#             quants.reserved_quantity-= self.product_uom_qty
            
    @api.model
    def create(self, vals):
        res = super().create(vals)
        if 'picking_id' in vals:
            picking = self.env['stock.picking'].browse([vals['picking_id']])
            product = self.env['product.product'].browse([vals['product_id']])
            if picking and not res.lot_id:
                if picking.picking_type_id.is_generate_lot and product.tracking == 'lot':
                    lot_name = self.env['ir.sequence'].next_by_code('lot.generation') or 'New'
                    dict = {'name': lot_name,
                            'product_id': vals['product_id'],
                            'po_id' : picking.purchase_id.id,
                            'company_id' : self.env.user.company_id.id,
#                             'ship_date' : picking.ship_date,
#                             'pallet_number': res.
#                             'hides':
#                             'demand_qty':  
                         }
                    lot = self.env['stock.production.lot'].create(dict)
                    res.lot_id = lot.id
            if res.lot_id:
                if res.pallet_number == 0 :
                    res.pallet_number = res.lot_id.pallet_number
                if res.hides == 0 :
                    res.hides = res.lot_id.hides
                
        return res    
    
    def write(self,vals):
        for record in self:
            res = super().write(vals)
            if 'qty_done' in vals:
                ship_date = record.picking_id.ship_date
                record.lot_id.ship_date = ship_date         
            if 'pallet_number' in vals:
                pallet_number = record.pallet_number
                record.lot_id.pallet_number = pallet_number     
            if 'hides' in vals:
                hides = record.hides
                record.lot_id.hides = hides
            return res
                
        
    def _create_and_assign_production_lot(self):
        """ Creates and assign new production lots for move lines."""
        lot_vals = []
        # It is possible to have multiple time the same lot to create & assign,
        # so we handle the case with 2 dictionaries.
        key_to_index = {}  # key to index of the lot
        key_to_mls = defaultdict(lambda: self.env['stock.move.line'])  # key to all mls
        for ml in self:
            key = (ml.company_id.id, ml.product_id.id, ml.lot_name)
            key_to_mls[key] |= ml
            if ml.tracking != 'lot' or key not in key_to_index:
                key_to_index[key] = len(lot_vals)
                lot_vals.append({
                    'company_id': ml.company_id.id,
                    'name': ml.lot_name,
                    'product_id': ml.product_id.id,
                    'supplier_id': ml.move_id.purchase_line_id.order_id.partner_id.id,
                    'po_id': ml.move_id.purchase_line_id.order_id.id
                })

        lots = self.env['stock.production.lot'].create(lot_vals)
        for key, mls in key_to_mls.items():
            mls._assign_production_lot(lots[key_to_index[key]].with_prefetch(lots._ids))  # With prefetch to reconstruct the ones broke by accessing by index


    def check_available_quantity(self, product_id, location_id, quantity, lot_id=None):
 
        self = self.sudo()
        rounding = product_id.uom_id.rounding
        quants = self.env['stock.quant']._gather(product_id, location_id, lot_id=lot_id)
        if rounding:
            if float_compare(quantity, 0, precision_rounding=rounding) > 0:
                # if we want to reserve
                available_quantity = sum(quants.filtered(lambda q: float_compare(q.quantity, 0, precision_rounding=rounding) > 0).mapped('quantity')) - sum(quants.mapped('reserved_quantity'))
                return available_quantity
            elif float_compare(quantity, 0, precision_rounding=rounding) < 0:
            # if we want to unreserve
                available_quantity = sum(quants.mapped('reserved_quantity'))
    
    

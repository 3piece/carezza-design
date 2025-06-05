# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError

from collections import OrderedDict, defaultdict
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
import logging

_logger = logging.getLogger(__name__)

class StockMoveLine(models.Model):

    _inherit = 'stock.move.line'
    
    pallet_number = fields.Integer(string='Pallet / Box / Roll')
    hides = fields.Integer()
    create_auto = fields.Boolean()
    position = fields.Char()
    supplier = fields.Char() #Added by Raymond
    material_desc = fields.Char() #Added by Raymond
    remark = fields.Char() #Added by Raymond
    coo = fields.Char() #Added by Raymond

    #Change PO No Format (Added by Raymond)
    formatted_po_id_name = fields.Char(compute='_compute_formatted_po_id_name')
    
    @api.depends('lot_id.po_id.name')
    def _compute_formatted_po_id_name(self):
        for record in self:
            po_name = record.lot_id.po_id.name if record.lot_id and record.lot_id.po_id else False
            if po_name and '-' in po_name:
                try:
                    year_month, running_number = po_name.split('-')
                    new_running_number = '00' + running_number   # Adding '00' as the prefix
                    record.formatted_po_id_name = f"{year_month}-{new_running_number}"
                except ValueError:
                    record.formatted_po_id_name = po_name   # fallback to original if split fails
            else:
                record.formatted_po_id_name = ''
    #=================================================================================
    
    @api.onchange('lot_id')
    def onchange_lot_id(self):
        if self.lot_id:
            origin_reserved = 0
            if self._origin:
                origin_reserved = self._origin.product_uom_qty
                # orig_quants = self.env['stock.quant'].sudo()._update_reserved_quantity(self, self.product_id, self.location_id, 0, self._origin.lot_id)
                # orig_quants = self.env['stock.quant'].sudo()._gather(self.product_id, self.location_id, self._origin.lot_id)
            self.pallet_number = self.lot_id.pallet_number
            self.hides = self.lot_id.hides
            self.position = self.lot_id.position
            self.supplier = self.lot_id.supplier #Added by Raymond
            self.remark = self.lot_id.remark #Added by Raymond
            self.material_desc = self.lot_id.material_desc #Added by Raymond
            self.coo = self.lot_id.coo #Added by Raymond
            
            context = self.env.context
            if 'default_picking_id' in context:
                if context['default_picking_id']:
                    picking_id = context['default_picking_id']
                    move_id = self.env['stock.move'].search([('product_id', '=', self.product_id.id),
                                                             ('picking_id', '=', picking_id)])
                    qty_need = move_id.product_uom_qty - move_id.reserved_availability + origin_reserved - move_id.quantity_done
                    # quants = self.env['stock.quant'].sudo()._gather(self.product_id, self.location_id, self.lot_id)  # TODO: Remove
                    available_quantity = self.check_available_quantity(self.product_id, self.location_id, qty_need,
                                                                       self.lot_id)
                    self.product_uom_qty = qty_need if available_quantity > qty_need else available_quantity
                else:
                    _logger.debug(f"New stock.picking - No default_picking_id set")
            else:
                # TODO: Review, this added as previous code had no provision for picking_id in case default_picking_id not found.
                _logger.warning(f"No default_picking_id found")



    @api.model
    def create(self, vals):
        res = super().create(vals)
        if 'create_auto' not in vals:
            if 'product_uom_qty' in vals: 
                if res.lot_id:
                    quants = self.env['stock.quant'].sudo()._gather(res.product_id,res.location_id,res.lot_id)  
                    current_reserved_quantity = quants.reserved_quantity
                    reserved_quantity = vals['product_uom_qty'] 
                    quants.reserved_quantity  = current_reserved_quantity + reserved_quantity      
        
        move_line_ids = self.env['stock.move.line'].search([('picking_id','=',res.picking_id.id),('move_id','=',res.move_id.id)])
        sum_reserved_quantity  = 0
        for line in move_line_ids:
            sum_reserved_quantity+= line.product_uom_qty          
        if sum_reserved_quantity > res.move_id.product_uom_qty:
            # TODO: Cleanup this code and check / validate it. Previously it wasn't running as it was incorrectly indented.
            res.product_uom_qty = 0
            #raise UserError("Product %s: Reserved can't > Demand"%res.product_id.display_name)
            # Check last record
            move_line_ids = self.env['stock.move.line'].search([('picking_id','=',res.picking_id.id),('move_id','=',res.move_id.id)])
            sum_reserved_quantity = 0
            for line in move_line_ids:
                sum_reserved_quantity+= line.product_uom_qty
            qty = res.move_id.product_uom_qty - sum_reserved_quantity
            if qty>0:
                res.product_uom_qty = qty
            else:
                res.product_uom_qty = 0
        
        
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
                            'ship_date' : picking.ship_date
                         }
                    lot = self.env['stock.production.lot'].create(dict)
                    res.lot_id = lot.id
            if res.lot_id:
                if res.pallet_number == 0 :
                    res.pallet_number = res.lot_id.pallet_number
                if res.hides == 0 :
                    res.hides = res.lot_id.hides
                if res.hides == 0 :
                    res.position = res.lot_id.position

                #Added by Raymond
                if not res.supplier :
                    res.supplier = res.lot_id.supplier
                if not res.remark :
                    res.remark = res.lot_id.remark
                if not res.material_desc :
                    res.material_desc = res.lot_id.material_desc
                if not res.coo :
                    res.coo = res.lot_id.coo
                #=====================
                
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
            if 'position' in vals:
                position = record.position
                record.lot_id.position = position

            #Added by Raymond
            if 'supplier' in vals:
                supplier = record.supplier
                record.lot_id.supplier = supplier     
            if 'remark' in vals:
                remark = record.remark
                record.lot_id.remark = remark     
            if 'material_desc' in vals:
                material_desc = record.material_desc
                record.lot_id.material_desc = material_desc     
            if 'coo' in vals:
                coo = record.coo
                record.lot_id.coo = coo
            #==========================
            
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
                    'po_id': ml.move_id.purchase_line_id.order_id.id,
                    #Added by Raymond
                    'supplier': ml.move_id.supplier,
                    'remark': ml.move_id.remark,
                    'material_desc': ml.move_id.material_desc,
                    'coo': ml.move_id.coo
                    #===========================
                })
        lots = self.env['stock.production.lot'].create(lot_vals)
        for key, mls in key_to_mls.items():
            mls._assign_production_lot(lots[key_to_index[key]].with_prefetch(lots._ids))  # With prefetch to reconstruct the ones broke by accessing by index

    def check_available_quantity(self, product_id, location_id, quantity, lot_id=None):
        available_quantity = 0
        rounding = product_id.uom_id.rounding if product_id.uom_id.rounding else 0.0001
        quants = self.env['stock.quant'].sudo()._gather(product_id, location_id, lot_id=lot_id)
        comparison = float_compare(quantity, 0, precision_rounding=rounding)
        if comparison > 0:
            # if we want to reserve
            total_quants = sum(quants.filtered(lambda q: float_compare(q.quantity, 0, precision_rounding=rounding) > 0).mapped('quantity'))
            origin_reserved = self._origin.product_uom_qty if self._origin and \
                                                              self._origin.lot_id == lot_id and \
                                                              self._origin.location_id == location_id and \
                                                              self._origin.product_id == product_id else 0
            available_quantity = total_quants - sum(quants.mapped('reserved_quantity')) + origin_reserved
        elif comparison < 0:
            # if we want to unreserve
            available_quantity = sum(quants.mapped('reserved_quantity'))
        _logger.debug(f'Available Qauntity: {available_quantity}')
        return available_quantity

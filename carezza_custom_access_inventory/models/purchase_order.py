# -*- coding: utf-8 -*-

import logging
from odoo.exceptions import AccessError, ValidationError
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    po_date = fields.Date(help="Date PO was created in Aspiring", String='PO Date')
    excel_template = fields.Binary()
    excel_template_name = fields.Char("Filename")
    upload_excel_file = fields.Binary()
    upload_excel_name = fields.Char("Filename")

    def update_exist_transfer(self,transfer,details):
        for move in transfer.move_ids_without_package:
            for detail in details:
                if move.product_id.id == int(detail['product_id']):
                    vals= {'product_id' : move.product_id.id,
                           'picking_id': transfer.id,
                           'move_id': move.id,
                           'product_uom_id': move.product_id.uom_id.id,
                           'qty_done': detail['done'],
                           'location_id': transfer.location_id.id,
                           'location_dest_id': transfer.location_dest_id.id,
                           'state': 'assigned',
                           'pallet_number': detail['pallet_number'],
                           'hides': detail['hides']}
                    move_line = self.env['stock.move.line'].create(vals)
                    move._action_confirm()
                    #move._action_done()
                    

    def check_transfer(self ,details):  
        # TODO:  will have logic check all line must have the same purchase_name
        transfer = self.env['stock.picking'].search([('origin','=',details[0]['purchase_name']),('state','=','assigned')])
        self.update_exist_transfer(transfer, details)

       
    def test_details_insert(self):
        details = [{
                    'purchase_name' : self.name,
                    'product': "brown wool",
                    'product_id': 463,
                    'done': 1,
                    'pallet_number': 1,
                    'hides': 10,}]
        self.check_transfer(details)   
    

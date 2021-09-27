
__version__ = "14.1.2"  # version.phase.model  (Odoo Version | Module version | Model updates since module/phase update)
__revision__ = "1.1.1"  # logic.views.formatting (Mods since Model update- Business Logic | XML Views | Spelling, ect.)
__copyright__ = "Copyright 2020, Strategic A.I."
__license__ = "StraiCo_lic_2020_01"
__author__ = "Long"
__email__ = "bugs@strai.co"
__status__ = "Production"
__metalink__ = 'https://strai.co/jrtx35fdg'
__docformat__ = 'Google Docs'

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class StockPicking(models.Model):

    _inherit = "stock.picking"

    purchase_order_id = fields.Many2one('purchase.order')
    
    
    @api.onchange('purchase_order_id')
    def onchange_purchase_order_id(self):
        list_product = []
        for po_line in self.purchase_order_id.order_line:
            list_product.append((0, 0, { 'name' :po_line.product_id .partner_ref,
                                        
                                        'location_id' : self.location_id.id,
                                        'location_dest_id' : self.location_dest_id.id,
                                        'product_id': po_line.product_id.id,
                                        'product_uom_qty' : po_line.product_qty,
                                        'product_uom' : po_line.product_uom,
                                        'picking_id': self.id}))
        self.update({'move_ids_without_package' : list_product,
                     'origin' : self.purchase_order_id.name,})
        
    
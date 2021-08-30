
__version__ = "14.1.2"  # version.phase.model  (Odoo Version | Module version | Model updates since module/phase update)
__revision__ = "1.1.1"  # logic.views.formatting (Mods since Model update- Business Logic | XML Views | Spelling, ect.)
__copyright__ = "Copyright 2020, Strategic A.I."
__license__ = "StraiCo_lic_2020_01"
__author__ = "Long"
__email__ = "bugs@strai.co"
__status__ = "Production"
__metalink__ = 'https://strai.co/jrtx35fdg'
__docformat__ = 'Google Docs'

from itertools import groupby
from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class StockMove(models.Model):

    _inherit = "stock.move"


    def do_unreserve(self):
        self.picking_id.do_unreserve()

    def button_validate (self):
        self.picking_id.button_validate()
         

    # override fuction to revent merge stock.move to tranfer
    def _assign_picking(self):
        """ Try to assign the moves to an existing picking that has not been
        reserved yet and has the same procurement group, locations and picking
        type (moves should already have them identical). Otherwise, create a new
        picking to assign them to. """
        
        
        Picking = self.env['stock.picking']
        grouped_moves = groupby(sorted(self, key=lambda m: [f.id for f in m._key_assign_picking()]), key=lambda m: [m._key_assign_picking()])
        for group, moves in grouped_moves:
            moves = self.env['stock.move'].concat(*list(moves))

            new_picking = True
            picking = Picking.create(moves._get_new_picking_values())
            moves.write({'picking_id': picking.id})
            moves._assign_picking_post_process(new=new_picking)
        return True

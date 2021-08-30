
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

class StockMove(models.Model):

    _inherit = "stock.move"


    def do_unreserve(self):
        self.picking_id.do_unreserve()

    def button_validate (self):
        self.picking_id.button_validate()
          

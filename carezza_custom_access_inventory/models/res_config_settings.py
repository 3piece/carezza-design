# -*- coding: utf-8 -*-
__license__ = "AEM_lic_2020_01"
__version__ = "13.01"  # version.phase
__revision__ = "01.01.01.01"  # model.logic.views.formatting
__docformat__ = 'reStructuredText'

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    days_of_supplies = fields.Many2one('helpdesk.team',
                                       config_parameter='helpdesk_backorder.helpdesk_team_id', string='Days of supplies')
    
    

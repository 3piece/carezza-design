# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging
from odoo.addons.purchase.controllers.portal import CustomerPortal
from odoo.http import request
from odoo import fields, http, SUPERUSER_ID, tools, _

class CustomerPortal(CustomerPortal):

    
    @http.route(['/my/purchase/<int:order_id>'], type='http', auth="public", website=True)
    def portal_my_purchase_order(self, order_id=None, access_token=None, **kw):
       response = super(CustomerPortal, self).portal_my_purchase_order(order_id, access_token, **kw) 
       response.qcontext['pickings'] = response.qcontext['order'].picking_ids
#        a = response.qcontext['picking_id']
       return response
       
       
       

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging
from odoo.addons.purchase.controllers.portal import CustomerPortal
from odoo.addons.web.controllers.main import ReportController
from odoo.http import request
from odoo import fields, http, SUPERUSER_ID, tools, _
import base64

class CustomerPortal(CustomerPortal):

    
    @http.route(['/my/purchase/<int:order_id>'], type='http', auth="public", website=True)
    def portal_my_purchase_order(self, order_id=None, access_token=None, **kw):
       response = super(CustomerPortal, self).portal_my_purchase_order(order_id, access_token, **kw) 
       if 'order' in response.qcontext:
           response.qcontext['pickings'] = response.qcontext['order'].picking_ids
#        a = response.qcontext['picking_id']
       return response
   
   
    @http.route('/picking_upload_csv', type='http', method='POST', auth="user",website=True)
    def picking_upload_csv(self,**post):
 
        file_name = post.get('attachment')
        picking_id = int(post.get('picking_id'))
#         a = ReportController
#         ReportController.report_download(ReportController,'["/report/pdf/lot_labels.lot_label_transfer_template_view_pdf/2542","qweb-pdf"]','dummy-because-api-expects-one','{"lang":"en_US","tz":"Hongkong","uid":2,"allowed_company_ids":[1]}')
        picking_id = request.env['stock.picking'].browse([picking_id])
        picking_id.ship_date = post.get('ship_date')
#         
#         report = request.env['ir.actions.report'].browse([385])
#         report._render_qweb_pdf([picking_id.id],{'context': {'tz': 'Hongkong', 'uid': 2, 'allowed_company_ids': [1]}})
#         
        if file_name != '':
            file = post.get('attachment')
            file_name = post.get('attachment',False).filename
            picking_id.upload_excel_file = base64.b64encode(file.read())
            picking_id.upload_excel_name = file_name
        
       
    @http.route('/print_lot_label', type='http', auth="user",website=True)
    def print_lot_label(self,**post):
        picking_id = post['picking_id']
        respone = ReportController.report_download(ReportController(),'["/report/pdf/lot_labels.lot_label_transfer_template_view_pdf/%s","qweb-pdf"]'%picking_id,'dummy-because-api-expects-one','{"lang":"en_US","tz":"Hongkong","uid":2,"allowed_company_ids":[1]}')
        return respone           
       

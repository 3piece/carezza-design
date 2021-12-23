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
           response.qcontext['pickings'] = response.qcontext['order'].picking_ids.filtered(lambda picking: picking.state not in [ 'draft','done','cancel'])
           stock_picking_types = request.env['stock.picking.type'].search([('code','=','incoming')])
           response.qcontext['stock_picking_types'] = stock_picking_types
       return response
          
    @http.route('/create_transfer', type='http', method='POST', auth="user",website=True)
    def create_transfer(self,**post):  
        order = request.env['purchase.order'].browse([int(post['order'])])
        picking_id = order.picking_ids.filtered(lambda picking: picking.state not in [ 'draft','done','cancel'])
        if picking_id:
            new_picking = picking_id[0].copy()
            new_picking.action_confirm()
            new_picking.ship_date = post.get('ship_date')
            url = (request.httprequest.referrer and request.httprequest.referrer + "#create-transfer")
            return request.redirect(url)
    
    @http.route('/picking_upload_csv', type='http', method='POST', auth="user",website=True)
    def picking_upload_csv(self,**post):
        file_name = post.get('attachment')
        picking_id = int(post.get('picking_id'))
        picking_id = request.env['stock.picking'].browse([picking_id])
        picking_id.ship_date = post.get('ship_date')
        picking_id.is_upload = True 
        if file_name != '':
            file = post.get('attachment')
            file_name = post.get('attachment',False).filename
            picking_id.upload_excel_file = base64.b64encode(file.read())
            picking_id.upload_excel_name = file_name
            url = (request.httprequest.referrer and request.httprequest.referrer + "#create-transfer")
            #return request.redirect(url)
       
    @http.route('/print_lot_label', type='http', auth="user",website=True)
    def print_lot_label(self,**post):
        picking_id = post['picking_id']
        respone = ReportController.report_download(ReportController(),'["/report/pdf/lot_labels.lot_label_transfer_template_view_pdf/%s","qweb-pdf"]'%picking_id,'dummy-because-api-expects-one','{"lang":"en_US","tz":"Hongkong","uid":2,"allowed_company_ids":[1]}')
        return respone           
       

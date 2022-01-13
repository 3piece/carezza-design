# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging
from collections import OrderedDict
from odoo.addons.portal.controllers.portal import pager as portal_pager, CustomerPortal
from odoo.addons.web.controllers.main import ReportController
from odoo.exceptions import AccessError,ValidationError
from odoo.http import request
from odoo import fields, http, SUPERUSER_ID, tools, _
import base64



class CustomerPortal(CustomerPortal):

    
    @http.route(['/my/purchase', '/my/purchase/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_purchase_orders(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        PurchaseOrder = request.env['purchase.order']

        domain = []

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc, id desc'},
            'name': {'label': _('Name'), 'order': 'name desc, id desc'},
            'amount_total': {'label': _('Total'), 'order': 'amount_total desc, id desc'},
        }
        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': [('state', 'in', ['purchase', 'done', 'cancel'])]},
            'purchase': {'label': _('Purchase Order'), 'domain': [('state', '=', 'purchase')]},
            'cancel': {'label': _('Cancelled'), 'domain': [('state', '=', 'cancel')]},
            'done': {'label': _('Locked'), 'domain': [('state', '=', 'done')]},
        }
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        # count for pager
        purchase_count = PurchaseOrder.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/purchase",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby},
            total=purchase_count,
            page=page,
            step=self._items_per_page
        )
        # search the purchase orders to display, according to the pager data
        orders = PurchaseOrder.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager['offset']
        )
        request.session['my_purchases_history'] = orders.ids[:100]

        values.update({
            'date': date_begin,
            'orders': orders,
            'page_name': 'purchase',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'default_url': '/my/purchase',
        })
        return request.render("purchase.portal_my_purchase_orders", values)
    
    
    @http.route(['/my/purchase/<int:order_id>'], type='http', auth="public", website=True)
    def portal_my_purchase_order(self, order_id=None, access_token=None, **kw):
       response = super(CustomerPortal, self).portal_my_purchase_order(order_id, access_token, **kw) 
       if 'order' in response.qcontext:
           response.qcontext['pickings'] = response.qcontext['order'].picking_ids.filtered(lambda picking: picking.state not in [ 'draft','done','cancel'])
           stock_picking_types = request.env['stock.warehouse'].search([])
           response.qcontext['stock_picking_types'] = stock_picking_types
       return response
          
    @http.route('/create_transfer', type='http', method='POST', auth="user",website=True)
    def create_transfer(self,**post):  
        order = request.env['purchase.order'].browse([int(post['order'])])
        picking_id = order.picking_ids.filtered(lambda picking: picking.state not in [ 'draft','done','cancel'])
        if picking_id:
            new_picking = picking_id[0].sudo().copy()
            
            new_picking.is_upload = False
            #new_picking.picking_type_id = int(post.get('operation_type_value'))
            new_picking.ship_date = post.get('ship_date')
            warehouse = request.env['stock.warehouse'].search([('id','=',post.get('operation_type_value'))])
            operation_type = warehouse.stock_po_picking_type_id
            if not operation_type:
                raise ValidationError('%s not set default operation, pls check in config warehouse'%warehouse.name)
            
            new_picking.location_id = operation_type.default_location_src_id.id
            new_picking.location_dest_id = operation_type.default_location_dest_id.id
            new_picking.picking_type_id = operation_type
            for stock_move in new_picking.move_ids_without_package:
                stock_move.location_id = operation_type.default_location_src_id.id
                stock_move.location_dest_id = operation_type.default_location_dest_id.id
            
            for stock_move_line in new_picking.move_line_ids_without_package:
                stock_move_line.location_id = operation_type.default_location_src_id.id
                stock_move_line.location_dest_id = operation_type.default_location_dest_id.id
            
                      
            url = (request.httprequest.referrer and request.httprequest.referrer + "#create-transfer")
            new_picking.action_confirm()
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
       

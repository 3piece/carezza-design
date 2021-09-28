# -*- coding: utf-8 -*-
from odoo import http

# class CarezzaCustomLayout(http.Controller):
#     @http.route('/carezza_custom_layout/carezza_custom_layout/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/carezza_custom_layout/carezza_custom_layout/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('carezza_custom_layout.listing', {
#             'root': '/carezza_custom_layout/carezza_custom_layout',
#             'objects': http.request.env['carezza_custom_layout.carezza_custom_layout'].search([]),
#         })

#     @http.route('/carezza_custom_layout/carezza_custom_layout/objects/<model("carezza_custom_layout.carezza_custom_layout"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('carezza_custom_layout.object', {
#             'object': obj
#         })
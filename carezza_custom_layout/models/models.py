# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class carezza_custom_layout(models.Model):
#     _name = 'carezza_custom_layout.carezza_custom_layout'
#	  _inherit = ''
	  _rec_name = 'field'
	  #by default _rec_name = name


#     field = fields.Char()
#     field = fields.Integer()
#     field = fields.Float(compute="_compute_field", store=True)
#     description = fields.Text()
#     field = fields.Date(string="")
#     field = fields.Datetime(string="")
#     field = fields.Selection([("key","value"),("key","value")], string="")
#     field = fields.Datetime(string="")
#     field = fields.Boolean(string="")
    #Used to store html, provides html widget
#     field = fields.Html(string="")
    #Use to store Img or Pdf
#     field = fields.Binary(string="")

#	  field = fields.Many2one("model name",string="")
#	  field = fields.One2many("model name",'field many2one',string="")
#	  field = fields.Many2many("model name", string="")
	# related must be the same type
#	  field = fields.Boolean(string="",related='field.field')
		
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

#     @api.model
#     def create(self, vals):
#         #logic code
#         current_record = super().create(vals)
#         #logic code
#         return current_record
    
#     @api.multi
#     def write(self, vals):
#         for record in self:
#             #logic code
#             return super.write(vals)
        
#     @api.multi
#     def unlink(self):
#         for record in self:
#             #logic code
#         return super().unlink() 

#     @api.onchange('field')
#     def onchange_field(self):
#         if self.field:
#             # Logic
#         return  
      
      # like onchange but use for compute field
#     @api.depends('fields')
#     def _compute_field(self):
#         for record in self:
#             # Logic
#         return
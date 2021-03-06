# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError,ValidationError
import pandas as pd
import base64
import io
import csv
from datetime import datetime, timedelta
import xlrd
import tempfile
import binascii
import openpyxl
import math

class StockPicking(models.Model):

    _inherit = 'stock.picking'

    ship_date = fields.Date(string="Ship Date", tracking=True)
    bl_number = fields.Char(string='B/L Number')
    is_propagation = fields.Boolean(related='picking_type_id.is_propagation')
    po_date = fields.Date(related='purchase_id.po_date')
    is_locked = fields.Boolean(default=False, help='When the picking is not done this allows changing the '
                               'initial demand. When the picking is done this allows '
                               'changing the done quantities.')
    excel_template = fields.Binary()
    excel_template_name = fields.Char("Template")
    upload_excel_file = fields.Binary(tracking=True)
    upload_excel_name = fields.Char("Filename")
    is_upload = fields.Boolean()
                
                
    def prepare_value_generate(self):
        list = []
        for move_line_id in self.move_line_ids_without_package:
            value = {}
            value['ship_date'] = move_line_id.picking_id.ship_date
            value['picking_name'] = move_line_id.picking_id.name
            value['product_name'] =  move_line_id.product_id.display_name
            value['qty_done'] = move_line_id.qty_done
            value['pallet_number'] = move_line_id.pallet_number
            value['hides'] = move_line_id.hides
            value['move_line_id'] = move_line_id.id
            list.append(value)
        return list


    def button_validate(self):
        res = super().button_validate()
        for move_line_id in self.move_line_ids_without_package:
            if move_line_id.lot_id:
                move_line_id.lot_id.pallet_number = move_line_id.pallet_number
                move_line_id.lot_id.hides = move_line_id.hides
                move_line_id.lot_id.position = move_line_id.position
                
        return res

    @api.onchange('move_ids_without_package')
    def onchange_move_ids_without_package(self):
        if self.is_propagation:
            procurement_group = self.env['procurement.group'].search(
                [('picking_id', '=', self.id)])
            for stock_move in self.move_ids_without_package:
                if stock_move.group_id:
                    procurement_group = stock_move.group_id

            if not procurement_group:
                if self.move_ids_without_package:
                    procurement_group_name = self.env['ir.sequence'].next_by_code(
                        'procurement.group')
                    procurement_group = self.env['procurement.group'].create({'name': procurement_group_name,
                                                                              'move_type': 'direct'})
            for stock_move in self.move_ids_without_package:
                stock_move.group_id = procurement_group.id


    def remove_move_line(self,transfer,list_move_line_id):
        list_remove = []
        for current_move_line_id in transfer.move_line_ids_without_package:
            if current_move_line_id.id not in list_move_line_id:
                current_move_line_id.unlink()

    def update_move_line(self,transfer,detail):
        for move in transfer.move_ids_without_package: 
            move_line = self.env['stock.move.line'].search([('picking_id','=',transfer.id),('id','=',detail['move_line_id'])])
            if move_line:
                move_line.write({'qty_done': detail['qty_done'],
                                 'pallet_number': detail['pallet_number'],
                                 'hides': detail['hides'],})
                return move_line.id
            else:
                return False                    
        
    def create_move_line(self,transfer,detail,list_id_updated):   
        for move in transfer.move_ids_without_package:
            if list_id_updated:
                if detail['move_line_id'] not in list_id_updated and move.product_id.id == detail['product_id']:
                    vals= {'product_id' : move.product_id.id,
                           'picking_id': transfer.id,
                           'move_id': move.id,
                           'product_uom_id': move.product_id.uom_id.id,
                           'qty_done': detail['qty_done'],
                           'location_id': transfer.location_id.id,
                           'location_dest_id': transfer.location_dest_id.id,
                           'state': 'assigned',
                           'pallet_number': detail['pallet_number'],
                           'hides': detail['hides']
                           }
                    move_line = self.env['stock.move.line'].create(vals)  
            else:
                if move.product_id.id == detail['product_id']:
                    vals= {'product_id' : move.product_id.id,
                               'picking_id': transfer.id,
                               'move_id': move.id,
                               'product_uom_id': move.product_id.uom_id.id,
                               'qty_done': detail['qty_done'],
                               'location_id': transfer.location_id.id,
                               'location_dest_id': transfer.location_dest_id.id,
                               'state': 'assigned',
                               'pallet_number': detail['pallet_number'],
                               'hides': detail['hides']
                               }
                    move_line = self.env['stock.move.line'].create(vals)                                  
            
        
    def process_move_line(self,transfer,detail,list_move_line_id = None):
        #remove
        self.remove_move_line(transfer,list_move_line_id)
        #update
        list_id_update = self.update_move_line(transfer,detail)
        #Create
        #self.create_move_line(transfer,detail,list_id_update)
        return list_id_update
        
    def check_transfer(self, list_obj, list_move_line_id=None):
        #response.qcontext['order'].picking_ids.filtered(lambda picking: picking.state not in [ 'draft','done','cancel'])
        #picking_ids = self.purchase_id
        
        list_id_updated=[]
        #Process remove and update create for Current Picking belong  PO
        for detail in list_obj:
            #transfer = self.env['stock.picking'].search([('id', '=', detail['picking_name'])])         
            picking_ids = detail['purchase_id'].picking_ids.filtered(lambda picking: picking.state not in [ 'draft','done','cancel'])
            if self.id in picking_ids.ids:
                id_updated = self.process_move_line(self, detail, list_move_line_id)   
                if id_updated: 
                    list_id_updated.append(id_updated)       
        for detail in list_obj:
            picking_ids = detail['purchase_id'].picking_ids.filtered(lambda picking: picking.state not in [ 'draft','done','cancel'])
            if self.id in picking_ids.ids:
                self.create_move_line(self,detail,list_id_updated)
        
        #Process remove and Create  current Picking not belong PO
        for detail in list_obj:      
            picking_ids = detail['purchase_id'].picking_ids.filtered(lambda picking: picking.state not in [ 'draft','done','cancel']).sorted(key=lambda r: r.id, reverse=True)
            if self.id not in picking_ids.ids and picking_ids:
                #self.remove_move_line(picking_ids[0],[0])
                picking_ids[0].ship_date = self.ship_date
                self.create_move_line(picking_ids[0],detail,False)
                             
                     
    def get_id_by_value(self,model,field_names,value):
        model = self.env['stock.move.line']   
        converted = {} 
        converters = {
        name: self.env['ir.fields.converter'].to_field(model, field)
        for name, field in model._fields.items()
        }
        converted[field_names], ws = converters[field_names]([{None: value}])
        return converted[field_names]
  
    def read_csv(self,upload_excel_file):
        fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        fp.write(binascii.a2b_base64(upload_excel_file))
        fp.seek(0)
        df = pd.read_excel(fp.name, engine='openpyxl')
        df = df.to_dict()
        count_lop = len(df['Hides'])
        list_move_line_id = []
        list_obj = []

        for index in range(count_lop):  
            if  not isinstance(df['Product Name'][index], str): 
                break;          
            #product_name = "[%s] "%df['Code'][index] + "%s "%df['Product Name'][index]+ "[%s]"+ df['Color'][index]
            #full_name = df['Display Name'][index]
            
            if  math.isnan(df['Box / Roll / Pallet No'][index]):
                box = 0
            else:
                box = df['Box / Roll / Pallet No'][index]

            if  math.isnan(df['Hides'][index]):
                hides = 0
            else:
                hides = df['Hides'][index]
            
            if  math.isnan(df['Quantity'][index]):
                quantity = 0
            else:
                quantity = df['Quantity'][index]
                       
            code=""
            if isinstance(df['Code'][index], str):
                code = '[%s] '%df['Code'][index]
            color=""
            if isinstance(df['Color'][index], str):
                color = ' (%s)'%df['Color'][index]
            full_name = code+ df['Product Name'][index]+ color

            product_id = self.env['product.product'].sudo().search(
                [('name', '=', df['Product Name'][index]),
                 ('attribute_value', '=', df['Color'][index])])[0].id
            # product_id = self.get_id_by_value(self.env['stock.move.line'],'product_id',full_name)
            #picking_name = self.get_id_by_value(self.env['stock.move.line'],'picking_id',obj[0])
            
            purchase_id = self.env['purchase.order'].search([('name','=',df['PO'][index])])
            if not isinstance(df['PO'][index], str):
                purchase_id = self.purchase_id
            if not purchase_id and not isinstance(df['PO'][index], str):
                raise ValidationError('%s not exist'%df['PO'][index])
            
            dict_val = {
            'index': index,
            'picking_name' : self.name,
            'purchase_id': purchase_id,
            'product_id': product_id,
            'qty_done': quantity,
            'pallet_number': box,
            'hides': hides,
            'move_line_id': int(df['Move line id'][index]) if math.isnan(df['Move line id'][index])!= True else False }
            list_obj.append(dict_val)
            if not math.isnan(df['Move line id'][index]):
                list_move_line_id.append(int(df['Move line id'][index]))

        return list_obj,list_move_line_id
                    
    def write(self, vals):   
        if 'upload_excel_file' in vals:
            if vals['upload_excel_file']:
                list_obj, list_move_line_id = self.read_csv(
                    vals['upload_excel_file'])
                for obj in list_obj:
                    if obj['move_line_id'] != 0:
                        for check_obj in list_obj:
                            if check_obj['move_line_id'] == obj['move_line_id'] and check_obj['index'] != obj['index']:
                                check_obj['move_line_id'] = 0
                
                self.check_transfer(list_obj,list_move_line_id) 
                vals['is_upload'] = True        
        vals['upload_excel_file'] = False
        res = super().write(vals)
        if 'ship_date' in vals:
            for stock_move_line in self.move_line_ids_without_package:
                ship_date = self.ship_date
                stock_move_line.lot_id.ship_date = ship_date 
                if ship_date:
                    self.scheduled_date = ship_date + timedelta(days=14)
                    
        #self.upload_excel_file = False            
        return res



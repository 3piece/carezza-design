# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class ResUsers(models.Model):

    _inherit = 'res.users'

    warehouse_ids =  fields.Many2many('stock.warehouse')
    location_ids =  fields.Many2many('stock.location')
    
    def add_warehouse(self,warehose_id):
        warehouse = self.env['stock.warehouse'].browse([warehose_id])
        warehouse.responsible_user_ids = [(4,self.id)]
        
        # Add user into operation type
        operatation_types = self.env['stock.picking.type'].search([('warehouse_id','=',warehose_id)])
        for operatation_type in operatation_types:
            operatation_type.responsible_user_ids = [(4,self.id)]
        # Add responsible user into location
        root_location = warehouse.view_location_id
        locations = self.env['stock.location'].search([])
        self.location_ids = [(4,root_location.id)]
       
        stock_location_locations = self.env.ref('stock.stock_location_locations').id  
        if stock_location_locations not in self.location_ids.ids:
            self.location_ids = [(4,stock_location_locations)]
             
        for location in locations:
            parent_path = location.parent_path.split("/")
            parent_path.remove('')
            if len(parent_path) > 2:
                if int(parent_path[1]) == root_location.id:
                    location.responsible_user_ids = [(4,self.id)]
                    self.location_ids = [(4,location.id)]
        
        
    def remove_warehouse(self,warehose_id):
        warehouse = self.env['stock.warehouse'].browse([warehose_id])
        warehouse.responsible_user_ids = [(3,self.id)]       
        
        # Remove user into operation type
        operatation_types = self.env['stock.picking.type'].search([('warehouse_id','=',warehose_id)])
        for operatation_type in operatation_types:
            operatation_type.responsible_user_ids = [(3,self.id)]
        
        # Remove responsible user into location    
        root_location = warehouse.view_location_id
        locations = self.env['stock.location'].search([])
        self.location_ids = [(3,root_location.id)]
        
        for location in locations:
            parent_path = location.parent_path.split("/")
            parent_path.remove('')
            if len(parent_path) > 2:
                if int(parent_path[1]) == root_location.id:
                    location.responsible_user_ids = [(3,self.id)]   
                    self.location_ids = [(3,location.id)]        
                
    def write(self,vals):
        print(self.warehouse_ids)

        if 'warehouse_ids' in vals:
            warehouse_add = []
            warehouse_remove = []
            a =  vals['warehouse_ids'][0][2]
            for warehouse_id in vals['warehouse_ids'][0][2]:
                new = True
                for check_warehouse_id in self.warehouse_ids:
                    if warehouse_id == check_warehouse_id.id:
                        new = False

                if new:
                    warehouse_add.append(warehouse_id)
#                     
            for warehouse_id in self.warehouse_ids :
                remove = True
                for check_warehouse_id in vals['warehouse_ids'][0][2]:
                    if warehouse_id.id == check_warehouse_id:
                        remove = False
                        break;
                if remove:
                    warehouse_remove.append(warehouse_id.id)
        
            for warehouse_id in warehouse_add:
                self.add_warehouse(warehouse_id)
                
            for warehouse_id in warehouse_remove:
                self.remove_warehouse(warehouse_id)  
   
            
        res = super().write(vals)
        return res



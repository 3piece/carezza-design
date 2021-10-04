# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class ResUsers(models.Model):

    _inherit = 'res.users'

    warehouse_ids =  fields.Many2many('stock.warehouse')
    
    
    def add_warehouse(self,warehose_id):
        warehouse = self.env['stock.warehouse'].browse([warehose_id])
        warehouse.responsible_user_ids = [(4,self.id)]
        
        # add user into operation type
        operatation_types = self.env['stock.picking.type'].search([('warehouse_id','=',warehose_id)])
        for operatation_type in operatation_types:
            operatation_type.responsible_user_ids = [(4,self.id)]
        
        
    def remove_warehouse(self,warehose_id):
        warehouse = self.env['stock.warehouse'].browse([warehose_id])
        warehouse.responsible_user_ids = [(3,self.id)]       

        operatation_types = self.env['stock.picking.type'].search([('warehouse_id','=',warehose_id)])
        for operatation_type in operatation_types:
            operatation_type.responsible_user_ids = [(3,self.id)]
                
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
            print("XXXXXXXXXXXX")
            print(warehouse_add)
            print(warehouse_remove)
        
            for warehouse_id in warehouse_add:
                self.add_warehouse(warehouse_id)
                
            for warehouse_id in warehouse_remove:
                self.remove_warehouse(warehouse_id)  
   
            
        res = super().write(vals)
        return res



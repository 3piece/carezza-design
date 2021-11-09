# -*- coding: utf-8 -*-

import logging
from odoo.exceptions import AccessError
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):

    _inherit = 'product.template'

    default_code = fields.Char(
        'Code', compute='_compute_default_code',
        inverse='_set_default_code', store=True)
    
    material_type = fields.Char(compute='compute_material_type', store=True)
    material_types = fields.Selection([('fabric','Fabric'),('spo_fabric','SPO Fabric '),('leather','Leather'),('ukfr_fabric','UKFR Fabric'),('accessories','Accessories')], string='Label Type')
       
    @api.depends('categ_id')
    def compute_material_type(self):
        for record in self:
            material_type = None
            categ_name = record.categ_id.parent_path.split('/')
            categ_name.remove('')
            if len(categ_name) > 1 :
                # 17 is ID Accessories
                if int(categ_name[1]) == 17:
                    material_type = "Accessories"
                # 18 = Material
                elif int(categ_name[1]) == 18:
                    if len(categ_name) == 2:
                        material_type = "Material"
                    else:
                        #    25 = Leather
                        if int(categ_name[2]) == 25:
                            material_type = "Leather"
                        else:
                            material_type = "Material"
                            
            record.material_type = material_type         
                    
#             a = categ_name
    
    
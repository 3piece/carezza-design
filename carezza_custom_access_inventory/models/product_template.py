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
    
    material_type = fields.Char()
    label_type = fields.Selection([('accessories_small','Accessories small'),('fabric','Fabric'),('spo_fabric','SPO Fabric'),('leather','Leather'),('ukfr_fabric','UKFR Fabric'),('accessories','Accessories')], string='Label Type', store=True)
      
    def copy(self, default=None):
        # TDE FIXME: should probably be copy_data
        #default['generate_id'] = False
        res = super(ProductTemplate, self).copy(default=default) 
        return res

    #Added by Raymond
    @api.model
    def get_display_value(self, stored_value):
        # Get the selection field definition
        field = self._fields['label_type']
        selection = dict(field.selection)

        # Retrieve the display value based on the stored value
        display_value = selection.get(stored_value, 'Unknown')
        if display_value == 'SPO Fabric' :
            display_value = 'Fabric'
        return display_value
    #=====================================
        
    @api.onchange('categ_id')
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

    @api.onchange('material_type')
    def compute_label_type(self):
        for rec in self:
            if rec.material_type == 'Material':
                rec.label_type = 'fabric'
            elif rec.material_type == 'Accessories':
                rec.label_type = 'accessories'
            elif rec.material_type == 'Leather':
                rec.label_type = 'leather'
            else:
                rec.label_type = None
                
    def re_generate_external_id(self):
        for rec in self:
            for product in rec.product_variant_ids:
                variant_att_name = ""
                for product_template_attribute_value_ids in product.product_template_attribute_value_ids:
                    variant_att_name+= '_'+ product_template_attribute_value_ids.name.strip().replace(' ', '_')
                
                variant_name = product.name.strip().replace(' ', '_')
                external_id = variant_name + variant_att_name
                external_id = external_id.replace('(', '').replace(')', '').replace(' ', '_').replace('.', '_')            
                
                ir_model_data = self.env['ir.model.data'].search([('res_id','=', product.id),
                                                                  ('model','=','product.product')])
                
                ir_model_data.sudo().name =  external_id

    def unlink(self):
        product_product_env = self.env['product.product']
        ir_model_data_env = self.env['ir.model.data']

        for template in self:
            # Get related product.product records
            product_ids = product_product_env.search([('product_tmpl_id', '=', template.id)])

            for product in product_ids:
                # Delete corresponding ir_model_data record
                xml_id = ir_model_data_env.search([('model', '=', 'product.product'), ('res_id', '=', product.id)])
                if xml_id:
                    xml_id.unlink()

        return super(ProductTemplate, self).unlink()

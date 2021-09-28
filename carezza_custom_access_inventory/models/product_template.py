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
    
    
class ProductTemplate(models.Model):

    _inherit = 'product.product'

    default_code = fields.Char('Code', index=True)


    def update_external_id(self,model, id, external_id, prefix='__export__', safe=True):
        model_data = self.env['ir.model.data']
        current_ids = model_data.search([('model', '=', model), ('res_id', '=', id)])
        if current_ids:
            _logger.info('Found %s external_ids for model: %s with id: %s', len(current_ids), model, id)
            if not safe:
                for existing_id in model_data.browse(current_ids):
                    _logger.info('Found external_id for model: %s, with id: %s, as: %s', model, id,
                                    existing_id.module + '.' + existing_id.name)
                updated_record = model_data.browse(current_ids[0])
                _logger.warning('Updating external_id for model: %s, with id: %s, from %s ==> %s',  model, id,
                                updated_record.module + '.' + updated_record.name, prefix + '.' + external_id)
                updated_record.module = prefix
                updated_record.name = external_id
            else:
                _logger.info('No external_id updated for model: %s with id: %s. To update, set safe=False',
                             len(current_ids), model, id)
        else:
            model_data.create({'name': external_id, 'module': prefix, 'model': model, 'res_id': id})
            _logger.info('Add external_id for model: %s, for id: %s, with external_id: %s', model, id,
                         prefix + '.' + external_id)
        return True

 
 
    def generate_external_ids(self):
        PRODUCT_PRODUCT_MATERIAL_PREFIX = "aspiring_import_product_product_variant"
        prefix = PRODUCT_PRODUCT_MATERIAL_PREFIX
        external_id_ids = self.env['ir.model.data'].search_read(domain=[('model', '=', 'product.product')], fields=['res_id'])
        print(external_id_ids)
        res_ids = [i['res_id'] for i in external_id_ids]
        print(res_ids)
        empty_ex_ids = self.env['product.product'].search(['!', ('id', 'in', res_ids)])
        # empty_ex_ids = self.env['product.product'].search([])
        # print(empty_ex_ids)
        # variants = self.env['product.product'].browse(empty_ex_ids[5])
        # for variant_id in empty_ex_ids:
        for variant_id in empty_ex_ids:
            variant = self.env['product.product'].browse(variant_id.id)
            if variant.product_template_attribute_value_ids:
                variant_name = variant.product_template_attribute_value_ids[0].name
                variant_name = self.env['product.product'].browse(variant_id).product_template_attribute_value_ids[0].name
                external_id = f'{variant.name}_{variant_name}'.strip().replace(' ', '_')
                # external_id = variant_name.replace('(', '').replace(')', '').strip().replace(' ', '_')
                print(external_id)
                update_external_id('product.product', variant_id, external_id, prefix)
            else:
                _logger.warning('No variant attribute value found for variant (product.product): %s, with ID: %s',
                                variant.display_name, variant.id)
     
        
    @api.model
    def create(self,vals):
        res = super().create(vals)
        res.generate_external_ids()
        return res
        
        
    
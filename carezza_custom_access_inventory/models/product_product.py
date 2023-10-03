# -*- coding: utf-8 -*-

import logging
from odoo.exceptions import AccessError
from odoo import models, fields, api, _


_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):

    _inherit = 'product.product'

    default_code = fields.Char('Code', index=True)
    attribute_value = fields.Char(related='product_template_attribute_value_ids.product_attribute_value_id.name', string='Color')

    def update_external_id(self,model, id, external_id, prefix='__export__', safe=True):
        model_data = self.env['ir.model.data']
        current_ids = model_data.search([('model', '=', model), ('res_id', '=', id.id)])
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
            model_data.sudo().create({'name': external_id, 'module': prefix, 'model': model, 'res_id': id.id})
            _logger.info('Add external_id for model: %s, for id: %s, with external_id: %s', model, id.id,
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
        for variant_id in empty_ex_ids:
            variant = self.env['product.product'].browse(variant_id.id)
            variant_att_name = ""
            for product_template_attribute_value_ids in variant.product_template_attribute_value_ids:
                variant_att_name+= '_'+product_template_attribute_value_ids.name.strip().replace(' ', '_')
                
            variant_name = variant.name.strip().replace(' ', '_')
#             variant_name = variant_name.replace('_(copy)', '')
            external_id = variant_name+variant_att_name
            external_id = external_id.replace('(', '').replace(')', '').replace(' ', '_').replace('.', '_')
            self.update_external_id('product.product', variant_id, external_id, prefix)

    @api.model
    def create(self,vals):
        res = super().create(vals)
        res.generate_external_ids()
        if not res.barcode:
            name=""
            if res.id < 10:
                name = "0000"
            elif res.id < 100:
                name = "000"
            elif res.id < 1000:
                name = "00"
            elif res.id < 10000:
                name = "0"
            res.barcode = name + str(res.id)
        return res

    def unlink(self):
        for record in self:
            xml_id = self.env['ir.model.data'].search([('model', '=', 'product.product'), ('res_id', '=', record.id)])
            if xml_id:
                xml_id.unlink()
        return super().unlink()

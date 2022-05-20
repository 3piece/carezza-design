import odoorpc
import logging
# import csv
import pandas as pd

_logger = logging.getLogger(__name__)


class OdooProcessor(object):

    def __init__(self):
        # host = '127.0.0.1'
        # port = '8014'
        # server_url = 'http://localhost:8014'
        # host = 'carezza-design.odoo.com'
        # db_name = 'car_22_S09_01'
        # username = 'admin'
        # password = 'admin'

        # Remember to change password on the server
        port = '443'  # 80
        # server_url = 'https://carezza-design-stag-v14-s2111-2633764.dev.odoo.com'
        host = 'carezza-design.odoo.com'
        db_name = '3piece-carezza-design-master-2586737'
        # host = 'carezza-design-uat-v14-s2202-6-4061662.dev.odoo.com'
        # db_name = 'carezza-design-uat-v14-s2202-6-4061662'
        username = 'admin'
        password = 'strategiccar253'

        self.odoo = odoorpc.ODOO(host=host, port=port, protocol='jsonrpc+ssl')  #protocol='jsonrpc'  - port 80
            # .login(db_name, username, password)

        self.odoo.login(db_name, username, password)  # login




    # print('hi')
    def get_user(self):
        # User information
        user = self.odoo.env.user
        print(user.name)
        return user

    # print(odoo.db.list())
    # Product = odoo.env['product.product']
    # Product.name_get([2])

    #  The following will not work as an update of name on product.product will update product.template name
    # product_ids = Product.search([])
    # for variant_id in product_ids:
    #     variant = Product.browse(variant_id)
    #     variant.name = variant.display_name.replace('(', '| ').replace(')', '')


    # Use all methods of a model
    # if 'sale.order' in odoo.env:
    #     Order = odoo.env['sale.order']
    #     order_ids = Order.search([])
    #     for order in Order.browse(order_ids):
    #         print(order.name)
    #         products = [line.product_id.name for line in order.order_line]
    #         print(products)

    # My code

    # def update_external_id(model, id, prefix, external_id, safe=True):
    #     module = '__export__'
    #     current_ids = self.env['ir.model.data'.search([('model', '=', 'model'), ('res_id', '=', 'id'), ('module', '=', module)])
    #         if current_ids and not safe:
    #             write ir_model_data ...
    #         else not current_ids
    #             creat ir_model_data ...
    #             .... self.env['ir.model.data'].write({'module'=module, 'model' = model, 'res_id' = id, 'name' = external_id})
    #
    # def generate_external_ids():
    #     prefix = "import_from_outside_product_variants"
    #     empty_ex_ids: self.env[product.product].search( find all product.product records without external_ids)
    #     for record in empty_ex_ids:
    #         attribute_name = record.attribute_ids.name
    #         attribute_value = record.attribute_ids.value
    #         new_external_id = "{}_{}_{}".format(record.name, attribute_name, attribute_value)
    #         update_external_id('product.product', record.id, prefix, new_external_id)

    # new code
    def update_external_id(self, model, id, external_id, prefix='__export__', safe=True):
        model_data = self.odoo.env['ir.model.data']
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

    # test_update = update_external_id('product.product', '2661', 'austria_b_colour_cobalt_23')
    # print(test_update)

    def generate_external_ids(self):
        PRODUCT_PRODUCT_MATERIAL_PREFIX = "aspiring_import_product_product_variant"
        prefix = PRODUCT_PRODUCT_MATERIAL_PREFIX
        external_id_ids = self.odoo.env['ir.model.data'].search_read(domain=[('model', '=', 'product.product')], fields=['res_id'])
        print(external_id_ids)
        res_ids = [i['res_id'] for i in external_id_ids]
        print(res_ids)
        empty_ex_ids = self.odoo.env['product.product'].search(['!', ('id', 'in', res_ids)])
        # empty_ex_ids = odoo.env['product.product'].search([])
        # print(empty_ex_ids)
        # variants = odoo.env['product.product'].browse(empty_ex_ids[5])
        # for variant_id in empty_ex_ids:
        for variant_id in empty_ex_ids:
            variant = self.odoo.env['product.product'].browse(variant_id)
            if variant.product_template_attribute_value_ids:
                variant_name = variant.product_template_attribute_value_ids[0].name
                variant_name = self.odoo.env['product.product'].browse(variant_id).product_template_attribute_value_ids[0].name
                external_id = f'{variant.name}_{variant_name}'.strip().replace(' ', '_')
                # external_id = variant_name.replace('(', '').replace(')', '').strip().replace(' ', '_')
                print(external_id)
                self.update_external_id('product.product', variant_id, external_id, prefix)
            else:
                _logger.warning('No variant attribute value found for variant (product.product): %s, with ID: %s',
                                variant.display_name, variant.id)


    def confirm_pos(self, purchase_order_ids):
        for purchase_order_id in purchase_order_ids:
            purchase_order = self.odoo.env['purchase.order'].browse(purchase_order_id)
            purchase_order.button_confirm()

    def generation_lot_ids(self, stock_picking):
        print('Generating Lots')
        stock_picking.action_confirm()
        for move in stock_picking.move_lines:
            print(f"Move Lines: {move.id}")
            for move_line in move.move_line_ids:
                print('move line lines')
                print(f'moveline Product: {move_line.product_id} | Reserved: {move_line.product_uom_qty} | '
                      f'Real Reserved: {move_line.product_uom_qty} | Done: {move_line.qty_done}')
                # lot_name = ''
        for move in stock_picking.move_ids_without_package:
            print("Move Lines sans Pack")
            for move_line in move.move_line_ids:
                print(f'moveline (sans Pack) Product: {move_line.product_id.name} | Reserved: {move_line.product_uom_qty} | '
                      f'Real Reserved: {move_line.product_uom_qty} | Done: {move_line.qty_done}')
                # lot_name = ''


    def confirm_receipts(self, stock_picking_ids, action='confirmed'):
        for stock_picking_id in stock_picking_ids:
            stock_picking = self.odoo.env['stock.picking'].browse(stock_picking_id)
            if action == 'confirmed':
                stock_picking.action_confirm()
                # pass
            elif action == 'assigned' or 'done':
                # self.generation_lot_ids(stock_picking)
                stock_picking.button_validate()
            # elif action == 'done'
            #     stock_picking.action_confirm()

    def get_internal_ids(self, model, external_ids):
        # prep_connection()
        external_id_ids = self.odoo.env['ir.model.data'].search_read(domain=[('model', '=', model), ('name', 'in', external_ids)],
                                                                fields=['name', 'res_id'])
        return external_id_ids

    def get_po_ids(self, external_ids):
        po_ids = self.odoo.env['purchase.order'].search(['!', ('id', 'in', external_ids)])
        return po_ids


    # ---------

    # for attribute in variant.attribute_line_ids:
    #     print(attribute.attibute_id.name)
    # for record_id in empty_ex_ids:
    #     variant = odoo.env['product.product'].browse(record_id)
    #
    #     attribute_name = record.attribute_ids.name
    #     attribute_value = record.attribute_ids.value
    #     new_external_id = "{}_{}_{}".format(record.name, attribute_name, attribute_value)
    #     test_update = update_external_id('product.product', '2661', 'austria_b_colour_cobalt_23')
    #     update`




    #  Longs code
    # def update_external_id(self, rec_id, model, module, prefix, safe=True):
    #         ir_model_data = self.env['ir.model.data'].search([('res_id', '=', rec_id), ('model', '=', model)])
    #         if not ir_model_data:
    #             self.env['ir.model.data'].create({'name': prefix,
    #                                               'module': module,
    #                                               'model': model,
    #                                               'res_id': rec_id})
    #         elif ir_model_data and not safe:
    #             domain = [('res_id', '=', rec_id), ('model', '=', model), ('module', '=', module)]
    #             self.env['ir.model.data'].search(domain).write({'name': prefix,
    #                                                             'module': module,
    #                                                             'model': model,
    #                                                             'res_id': rec_id})
    #
    #     @api.model
    #     def generate_external_ids(self):
    #         prefix = "import_from_outside_product_variants"
    #         records = self.env['product.product'].search([])
    #         for rec in records:
    #             ir_model_data = self.env['ir.model.data'].search([('res_id', '=', rec.id), ('model', '=', 'product.product')])
    #             if not ir_model_data:
    #                 attribute_value = ""
    #                 for attribute_value in rec.product_template_attribute_value_ids:
    #                     if attribute_value:
    #                         attribute_value = '_' + \
    #                             attribute_value.name.replace(" ", "_")
    #                 prefix = prefix + '_' + rec.name + attribute_value
    #                 self.update_external_id(
    #                     rec.id, 'product.product', '__export__', prefix, safe=False)

    # load CSV file
    # with open('../output_2/purchase.order.csv', newline='') as csvfile:
    def load_csv_file(self, csv_file):
        # TODO: Check csv_file exits and report if not found
        csv_dict = ''
        with open(csv_file, newline='') as csvfile:
            csv_dict = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for purchase_order in csv_dict:
            print('Purchase Order: {} is {}'.format(purchase_order['id'], purchase_order['status_switch']))
        return csv_dict


    # def load_csv_to_pandas(file):


    # def load_po_file():
    #     po_file = '/home/pi3ce/03_DevProjects/carezza/carezza-design/import_assist/output_2/purchase.order.csv'
    #     purchase_orders = load_csv_file(po_file)
    #
    #     with open(po_file, newline='') as csvfile:
    #         purchase_orders = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    #         return purchase_orders
    #         return external_ids

            # print('Purchase Order External_ids: {}'.format(po_ids))
            # for purchase_order in purchase_orders:
            #     print('Purchase Order: {} is {}'.format(purchase_order['id'], purchase_order['status_switch']))

    def split_list(list, seperator='.'):
        left_elements = []
        right_elements = []
        for i in list:
            left_elements.append(i.split(seperator)[0])
            right_elements.append(i.split(seperator, 1)[1])
        return left_elements, right_elements

    def process_pos(self):
        root_path = '/home/odoo/imports/'
        working_path = f'{root_path}origin/working/'
        po_file = f'{working_path}purchase.order.csv'

        print(f'Processing POs from: {po_file}')

        df = pd.read_csv(po_file, usecols=['id', 'status_switch'], sep=';')
        # purchase_orders = load_csv_file(po_file)
        # external_ids = [purchase_order['id'] for purchase_order in purchase_orders]
        # external_ids = df[(df['status_switch'] == 'confirmed'), 'id', 'status_switch'].to_string()

        # slow method
        external_ids = df[(df.status_switch == 'confirmed') | (df.status_switch == 'completed')]['id'].to_list()

        # Faster
        # values_to_filter = ['confirmed', 'completed']  # 'new'
        # external_ids = df[df.s`tatus_switch(values_to_filter)].to_string()
        # external_ids['id']

        # print(df.to_string())
        # print(df['status_switch'].unique())


        # print(split_list(external_ids)[1])
        # get_internal_ids('', split_list(external_ids)[1])

        # print(external_ids)
        # for

        # ext_ids = [i.split('.', 1)[1] for i in external_ids]  # Ok

        # ext_ids = [k for i in external_ids for j in i.split('.')[0]]

        # print('Purchase Order External IDs: {}'.format(for_ids))
        # print('Purchase Order External IDs: {}'.format(external_ids))


        eid_ids = self.get_internal_ids('purchase.order', [i.split('.', 1)[1] for i in external_ids])
        internal_ids = [d['res_id'] for d in eid_ids]  # Get list of values from dict (none missing)
        # eid_ids = get_internal_ids('purchase.order', split_list(external_ids)[1])  # OK
        # print('Purchase Order IDs: {}'.format(eid_ids))

        print(internal_ids)
        self.confirm_pos(internal_ids)

        # eid_ids = get_po_ids(external_ids)
        # print(get_po_ids(external_ids))

    #  --====----



    def process_receipts(self):
        po_file = '/home/pi3ce/03_DevProjects/carezza_dev/carezza-design/import_assist/output_3/purchase.order.stock.picking.csv'
        print(f'Processing Reciepts from: {po_file}')

        df = pd.read_csv(po_file, usecols=['id', 'state'], sep=';')

        # slow method - probably can process all records.
        external_ids = df[(df.state == 'confirmed') | (df.state == 'assigned')]['id'].to_list()

        eid_ids = self.get_internal_ids('stock.picking', [i.split('.', 1)[1] for i in external_ids])
        internal_ids = [d['res_id'] for d in eid_ids]  # Get list of values from dict (none missing)
        # print('Purchase Order IDs: {}'.format(eid_ids))

        print(internal_ids)
        self.confirm_receipts(internal_ids, 'confirmed')

        #process done receipts
        external_ids = df[(df.state == 'done')]['id'].to_list()

        eid_ids = self.get_internal_ids('stock.picking', [i.split('.', 1)[1] for i in external_ids])
        internal_ids = [d['res_id'] for d in eid_ids]  # Get list of values from dict (none missing)
        # print('Purchase Order IDs: {}'.format(eid_ids))

        print(internal_ids)
        self.confirm_receipts(internal_ids, 'done')



    # def link_po_receipts():
    #     purchase_order_ids
    #     for purchase_order_id in purchase_order_ids:
    #         purchase_order = odoo.env['purchase.order'].browse(purchase_order_id)
    #         purchase_order.button_confirm()



    # process_pos()
    # process_receipts()
    # generate_external_ids()
    # link_po_receipts()


    # odoo = ''


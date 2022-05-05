# -*- coding: utf-8 -*-
#################################################################################
# Author      : Strategic A.I. Company Limited (<https://strai.co/>)
# Copyright(c): 2015-Present Strategic A.I. Company Limited
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.strai.co/license.html/>
#################################################################################
{
    'name': "Stock Maximize Lot Qaunts",

    'summary': """

        During a transfer, if using lot number, press the button to set reserved quantities to the maximum for that 
        all lots in the transfer.""",

    'description': """
        Strategic AI Stock Maximize Lot Qaunts
        ==========================

       During a transfer, if using lot number, press the button to set reserved quantities to the maximum for that
       all lots in the transfer


        You can manage:
        ---------------
        lots

    """,

    'author': "Strategic A.I.",
    'website': "https://strai.co",
    'category': 'Inventory',
    'version': '14.0.1.0.1',
    'application':  False,
    'installable':  True,
    'auto_install':  False,
    'price': 1290,
    'currency': 'USD',
    'license': 'Other proprietary',
    'sequence': 40,
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml

    'depends': ['base', 'stock'],

    'data': [
         # 'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
        # 'views/templates.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
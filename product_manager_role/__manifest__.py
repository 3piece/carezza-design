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
    'name': "Product Manager",  # THIS MUST BE CHANGED BEFORE PUSHING FIRST COMMIT !!!

    'summary': """ Product Manager""",

    'description': """
	  add Product manager role in User setting
    """,

    'author': "Strategic A.I.",
    'website': "https://strai.co",

    'category': 'Inventory',
    'version': '14.0.0.0.0',
    'application':  True,
    'installable':  True,
    'auto_install':  False,
    'price': 100,
    'currency': 'USD',
    'license': 'Other proprietary',
    'sequence': 40,
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml

    'depends': ['base','product','stock','purchase'],

    'data': [
        
        'security/group_security.xml',
        'security/ir.model.access.csv',
        
        
        
    ],

    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}

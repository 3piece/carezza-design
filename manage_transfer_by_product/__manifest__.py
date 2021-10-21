# -*- coding: utf-8 -*-
{
    'name': 'Manage Transfer By Product',
    'version': '14.0.0.2',
    'summary': 'Manage Transfer By Product',
    'description': """
        Manage Transfer By Product
    """,

    'author': "Strategic A.I.",
    'website': "https://strai.co",
    'sequence': 40,

    'category': 'Uncategorized',
    'application':  True,
    'installable':  True,
    'auto_install':  False,
    'price': 150,
    'currency': 'USD',
    'license': 'Other proprietary',
    # any module necessary for this one to work correctly
    'depends': ['base','stock','purchase'],

    # always loaded
    'data': [
         'views/stock_move.xml',
         'views/stock_picking.xml',
         
    ],
    # only loaded in demonstration mode
#     'demo': [
#         'demo/demo.xml',
#     ],
}

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
    'name': "Cron run import",

    'summary': """
        Cron run import.""",

    'description': """
        Cron run import.
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

    'depends': ['base','product'],

    'data': [        
        'data/product_cron.xml',             
    ],
    'qweb': [
        
    ],
    'demo': [
    ],
}

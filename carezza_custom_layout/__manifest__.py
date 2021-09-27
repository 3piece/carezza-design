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
    'name': "Carezza Custom Layout",  # THIS MUST BE CHANGED BEFORE PUSHING FIRST COMMIT !!!

    'summary': """

        IF YOU HAVE NOT REPLACED THIS SUMMARY TEXT AND WRITTEN AT LEAST 2 LINES, THEN YOUR COMMIT WILL BE VOID.

        (SAMPLE TEXT) Easily receive, store, sell, manage and convert products in various package / container sizes,
        using a single primary product for ease of management.
        Ease the process of purchasing products in different sizes / bulk package options via the website.
        No more tyring to calculate 10000's of units of an item when transferring stock in larger containers.""",

    'description': """
        Strategic AI xxxxxx Management
        ==========================

        IF YOU HAVE NOT REPLACED THIS DESCRIPTION TEXT AND WRITTEN AT LEAST 4 LINES, THEN YOUR COMMIT WILL BE VOID.

        (SAMPLE TEXT) Advanced Product Packages allows defining a single product with that can be stored in multiple
        package options. Each package type acts as an independent product that can be stored, picked and sold.
        Packages can be converted from one type to another.
        Stock is managed by package units, and the system knows how many total units of the final product you have
        available.
        There are included conversion tools that automate BOM creation.
        A single product is managed on the e-commerce site, and can be sold in different package options at different
        prices.


        You can manage:
        ---------------
        * x
        * y
        * z


    """,

    'author': "Strategic A.I.",
    'website': "https://strai.co",

    'category': 'Inventory',
    'version': '14.0.1.0.1',
    'application':  True,
    'installable':  True,
    'auto_install':  False,
    'price': 1290,
    'currency': 'USD',
    'license': 'Other proprietary',
    'sequence': 40,
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml

    'depends': ['base','stock'],

    'data': [
         # 'security/ir.model.access.csv',
        'security/stock_security.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
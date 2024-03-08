# -*- coding: utf-8 -*-
{
    'name': "Barcode lines sequences",
    'summary': """
        Add sequences for scanned barcode line
    """,
    'description': """
        This module adds sequences number in each barcode line scanned
    """,
    'category': 'Inventory/Inventory',
    'version': '14.0.1.0',
    'depends': ['stock_barcode'],
    'qweb': [
        'static/src/xml/qweb_templates.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}

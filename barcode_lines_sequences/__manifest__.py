# -*- coding: utf-8 -*-
{
    'name': "Barcode lines sequences",
    'summary': """
        Add sequences for scanned barcode line
    """,
    'description': """
        This module adds sequences number in each barcode line scanned.
        Adjusted the sorting logic for barcode lines so that the last scanned barcode appears at the top.
    """,
    'category': 'Inventory/Inventory',
    'version': '14.0.2.0',
    'depends': ['stock_barcode'],
    'data': [
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/qweb_templates.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}

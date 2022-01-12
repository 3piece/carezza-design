# -*- coding: utf-8 -*-

""""product_template.py: Description of what x does."""



__version__ = "13.1.2"  # version.phase.model  (Odoo Version | Module version | Model updates since module/phase update)
__revision__ = "2.1.2"  # logic.views.formatting (Mods since Model update- Business Logic | XML Views | Spelling, ect.)
__copyright__ = "Copyright 2020, Strategic A.I."
__license__ = "StraiCo_lic_2020_01"
__author__ = "James Moyle, Long"
__email__ = "bugs@strai.co"
__status__ = "Production"
__metalink__ = 'https://strai.co/jrtx35fdg'
__docformat__ = 'Google Docs'


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import math


import argparse
from pathlib import Path
from subprocess import run
from shutil import move
from datetime import datetime, timedelta

# from .cron_import import convert_receipts
# from .cron_import import convert_po
from .import_commander import run_stack


# def move_file(input_foldeder, input_file, output_folder):
#
#     return True
#
# def archive_files(input_foldeder, input_files, output_folder):
#     for file in input_files:
#         move_file(input_foldeder, file, output_folder)
#     return True

# python ./import_commander.py -i ../origin/source_files/ -o ../output_3/



class ProductTemplate(models.Model):
    _inherit = 'product.template'

                                
    @api.model
    def cron_import(self):          
        run_stack()

        
        
            
    
        

# Copyright 2017 Creu Blanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class PartnerXlsx(models.AbstractModel):
    _name = "report.report_xlsx.stock_picking_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Partner XLSX Report"



    def generate_xlsx_report(self, workbook, data, pickings):
        bold = workbook.add_format({"bold": True})
        bold1 = workbook.add_format({"bold": True,
                                    "hidden": True})
        sheet = workbook.add_worksheet("Report")
        
        i = 1
        # Set width for header
        sheet.set_column(0, 0, 40)
        sheet.set_column(0, 1, 40)
        sheet.set_column(0, 2, 20)
        sheet.set_column(0, 3, 20)
        sheet.set_column(0, 4, 20)
        sheet.set_column(0, 5, 20)
        #sheet.set_column('A', None, None, {'hidden': True})
        # Set Header
        sheet.write(0, 0, "Picking Name", bold1)
        sheet.write(0, 1, "Code", bold)
        sheet.write(0, 2, "Product Name", bold)
        sheet.write(0, 3, "Color", bold)
        sheet.write(0, 4, "Demand Qty", bold)
        sheet.write(0, 5, "Box / Roll / Pallet No", bold)
        sheet.write(0, 6, "Hides", bold)
        sheet.write(0, 7, "Move line id", bold)
        sheet.write(0, 8, "Display Name", bold)
        
        
        
        for obj in pickings:
            row = 1
            
            for move_line in obj.move_line_ids_without_package:
                col = 0         
                sheet.write(row, col, obj.name)
                col += 1
                sheet.write(row, col, move_line.product_id.default_code)
                col += 1
                sheet.write(row, col, move_line.product_id.name)
                col += 1
                sheet.write(row, col, move_line.product_id.attribute_value)
                col += 1
                sheet.write(row, col, move_line.qty_done)
                col += 1
                sheet.write(row, col, move_line.pallet_number)
                col += 1
                sheet.write(row, col, move_line.hides)
                col += 1
                sheet.write(row, col, move_line.id)
                col += 1
                sheet.write(row, col, move_line.product_id.display_name)
                row +=1
        sheet.set_column('I:I', None, None, {'hidden': True})
    
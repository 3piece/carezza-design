# Copyright 2017 Creu Blanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class PartnerXlsx(models.AbstractModel):
    _name = "report.report_xlsx.stock_picking_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Partner XLSX Report"



    def generate_xlsx_report(self, workbook, data, pickings):
        bold = workbook.add_format({"bold": True})
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
        sheet.write(0, 0, "Picking Name", bold)
        sheet.write(0, 1, "PO", bold)
        sheet.write(0, 2, "Code", bold)
        sheet.write(0, 3, "Product Name", bold)
        sheet.write(0, 4, "Color", bold)
        sheet.write(0, 5, "Quantity", bold)
        sheet.write(0, 6, "Box / Roll / Pallet No", bold)
        sheet.write(0, 7, "Hides", bold)
        sheet.write(0, 8, "Supplier", bold) #Added by Raymond
        sheet.write(0, 9, "Description", bold) #Added by Raymond
        sheet.write(0,10, "Origin", bold) #Added by Raymond
        sheet.write(0,11, "Remark", bold) #Added by Raymond
        sheet.write(0,12, "Move line id", bold)
        
        
        for obj in pickings:
            row = 1
            
            for move_line in obj.move_line_ids_without_package:
                col = 0         
                sheet.write(row, col, obj.name)
                col += 1
                sheet.write(row, col, obj.purchase_id.name)
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
                #Added by Raymond
                if move_line.supplier:
                    sheet.write(row, col, move_line.supplier.upper())
                else:
                    sheet.write(row, col, obj.partner_id.company_name.upper())
                col += 1
                if move_line.material_desc:
                    sheet.write(row, col, move_line.material_desc.upper())
                else:
                    stored_value = move_line.product_id.product_tmpl_id.label_type
                    display_value = move_line.product_id.product_tmpl_id.get_display_value(stored_value)
                    sheet.write(row, col, display_value.upper())
                col += 1
                if move_line.coo:
                    sheet.write(row, col, move_line.coo.upper())
                else:
                    sheet.write(row, col, obj.partner_id.country_id.name.upper())
                col += 1
                if move_line.remark:
                    sheet.write(row, col, move_line.remark)
                col += 1                
                #===================
                sheet.write(row, col, move_line.id)
                row += 1
        sheet.set_column('M:M', None, None, {'hidden': True}) #Updated by Raymond

    
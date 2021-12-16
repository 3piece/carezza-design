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
        # Set Header
        sheet.write(0, 0, "Picking Name", bold)
        sheet.write(0, 1, "Product Name", bold)
        sheet.write(0, 2, "Demand Qty", bold)
        sheet.write(0, 3, "Box / Roll / Pallet No", bold)
        sheet.write(0, 4, "Hides", bold)
        sheet.write(0, 5, "Move line id", bold)
        
        for obj in pickings:
            row = 1
            
            for move_line in obj.move_line_ids_without_package:
                col = 0         
                sheet.write(row, col, obj.name)
                col += 1
                sheet.write(row, col, move_line.product_id.display_name)
                col += 1
                sheet.write(row, col, move_line.qty_done)
                col += 1
                sheet.write(row, col, move_line.pallet_number)
                col += 1
                sheet.write(row, col, move_line.hides)
                col += 1
                sheet.write(row, col, move_line.id)
                row += 1

            
    def generate_main_content(self, objects, sheet):
        sheet.set_column(0, 3, 20)  # Set the width of Column A to C  to 20.
        sheet.set_column(4, 4, 15)
        sheet.set_column(5, 16, 15)

        sheet.set_row(2, 25)  # Set the high of row 2  to 23.

        sheet.write(0, 0, "Report", self.format_bold_header)
        sheet.write(2, 0, "Project", self.format_table_bold_center_bg)
        sheet.write(2, 1, "Modified On", self.format_table_bold_center_bg)
        sheet.write(2, 2, "Opportunity", self.format_table_bold_center_bg)
        sheet.write(2, 3, "Potential Customer",
                    self.format_table_bold_center_bg)
        sheet.write(2, 4, "Province", self.format_table_bold_center_bg)
        sheet.write(2, 5, "Region", self.format_table_bold_center_bg)
        sheet.write(2, 6, "Contract Code", self.format_table_bold_center_bg)
        sheet.write(2, 7, "Projected Sales (Opportunity)",
                    self.format_table_bold_center_bg)
        sheet.write(2, 8, "Invoice Date", self.format_table_bold_center_bg)
        sheet.write(2, 9, "Sales Cycle Stage ",
                    self.format_table_bold_center_bg)
        sheet.write(2, 10, "Invoice Amount", self.format_table_bold_center_bg)
        sheet.write(2, 11, "Opp GP (%)", self.format_table_bold_center_bg)
        sheet.write(2, 12, "Term (Opportunity)",
                    self.format_table_bold_center_bg)
        sheet.write(2, 13, "Owner", self.format_table_bold_center_bg)
        sheet.write(2, 14, "Division (Opportunity)",
                    self.format_table_bold_center_bg)
        sheet.write(2, 15, "Product Category (Opportunity)",
                    self.format_table_bold_center_bg)
        sheet.write(2, 16, "Currency (Opportunity)",
                    self.format_table_bold_center_bg)

        row = 4
        set_width_row = 3
        for record in objects:
            sheet.set_row(set_width_row, 25)

            sheet.write('A' + str(row),
                        record.crm_project_id.name or "None", self.format_left)
            sheet.write('B' + str(row), record.write_date or "None",
                        self.format_right_datetime)
            sheet.write(
                'C' + str(row), record.crm_opportunity_id.name or "None", self.format_left)
            sheet.write(
                'D' + str(row), record.potential_customer_id.name or "None", self.format_left)
            sheet.write('E' + str(row),
                        record.province_id or "None", self.format_left)
            sheet.write('F' + str(row),
                        record.region_id.name or "None", self.format_left)
            sheet.write(
                'G' + str(row), record.crm_opportunity_id.contract_code or "None", self.format_left)
            sheet.write(
                'H' + str(row), record.crm_opportunity_id.contract_value or 0, self.format_right_number)
            sheet.write('I' + str(row), str(record.invoice_date)
                        [0:10] or "None", self.format_right)

            sheet.write(
                'J' + str(row), record.sale_cycle_stage_percentage or 0, self.format_right_percent)
            sheet.write('K' + str(row), record.invoice_amount or 0,
                        self.format_right_number)
            sheet.write('L' + str(row), record.opp_gp_pct or 0,
                        self.format_right_number)
            sheet.write(
                'M' + str(row), record.crm_opportunity_id.term or "None", self.format_left)
            sheet.write('N' + str(row),
                        record.owner_id.name or "None", self.format_left)
            sheet.write('O' + str(row),
                        record.division_id.name or "None", self.format_left)
            sheet.write('P' + str(row),
                        record.prod_root_id.name or "None", self.format_left)
            sheet.write(
                'Q' + str(row), record.crm_opportunity_id.currency_id.name or " ", self.format_left)
            row += 1
            set_width_row += 1
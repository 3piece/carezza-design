# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import csv

from odoo import models


class PartnerCSV(models.AbstractModel):
    _name = "report.base_report_csv.partner_csv"
    _inherit = "report.base_report_csv.abstract"
    _description = "Report Partner to CSV"

    def generate_csv_report(self, writer, data, partners):
        writer.writeheader()
        for obj in partners:
            writer.writerow({"name": obj.name, "email": obj.email})

    def csv_report_options(self):
        res = super().csv_report_options()
        res["fieldnames"].append("name")
        res["fieldnames"].append("email")
        res["delimiter"] = ";"
        res["quoting"] = csv.QUOTE_ALL
        return res
    
class StockPickingCSV(models.AbstractModel):
    _name = "report.base_report_csv.stock_picking_csv"
    _inherit = "report.base_report_csv.abstract"
    _description = "Report Stock Picking to CSV"

    def generate_csv_report(self, writer, data, partners):
        writer.writeheader()
        for obj in partners:
            writer.writerow({"name": obj.name, "partner_id": obj.partner_id})

    def csv_report_options(self):
        res = super().csv_report_options()
        res["fieldnames"].append("name")
        res["fieldnames"].append("partner_id")
        res["delimiter"] = ";"
        res["quoting"] = csv.QUOTE_ALL
        return res    
    
    

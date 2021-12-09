import csv

from odoo import models

class StockPickingCSV(models.AbstractModel):
    _name = "report.base_report_csv.stock_picking_csv"
    _inherit = "report.base_report_csv.abstract"
    _description = "Report Stock Picking to CSV"

    def generate_csv_report(self, writer, data, partners):
        writer.writeheader()
        for obj in partners:
            for move_line in obj.move_line_ids_without_package:
                writer.writerow({"Picking Name": obj.name,
                                 "Product Name": move_line.product_id.display_name,
                                 "Demand Qty": move_line.qty_done,
                                 "Box / Roll / Pallet No": move_line.pallet_number,
                                 "Hides": move_line.hides,
                                 "Move line id": move_line.id})
                           
    def csv_report_options(self):
        res = super().csv_report_options()
        res["fieldnames"].append("Picking Name")
        res["fieldnames"].append("Product Name")
        res["fieldnames"].append("Demand Qty")
        res["fieldnames"].append("Box / Roll / Pallet No")
        res["fieldnames"].append("Hides")
        res["fieldnames"].append("Move line id")
        res["delimiter"] = ","
        res["quoting"] = csv.QUOTE_ALL
        return res    
    
    

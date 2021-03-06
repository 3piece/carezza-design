# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import json
import logging
import operator

from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.addons.web.controllers.main import CSVExport, ExcelExport
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class DelayExport(models.Model):

    _name = "delay.export"
    _description = "Allow to delay the export"

    user_id = fields.Many2one("res.users", string="User", index=True)

    @api.model
    def delay_export(self, data):
        params = json.loads(data.get("data"))
        if not self.env.user.email:
            raise UserError(_("You must set an email address to your user."))
        self.with_delay().export(params)

    @api.model
    def _get_file_content(self, params):
        export_format = params.get("format")

        #  FIXME: itemgetter does not seem to be working with the given params and fields.
        # item_names = ("model", "fields", "ids", "domain", "import_compat", "context")
        # items = ""
        # try:
        #     items = operator.itemgetter(item_names)(params)
        # except KeyError as k:
        #     _logger.error("Key Error thrown, e: %s", k)
        # except Exception as e:
        #     _logger.error("Error thrown, e: %s", e)
        # model_name, fields_name, ids, domain, import_compat, context = items
        model_name = params['model']
        fields_name = params['fields']
        ids = params['ids']
        domain = params['domain']
        import_compat = params['import_compat']
        context = params['context']

        model = self.env[model_name].with_context(
            import_compat=import_compat, **context
        )
        records = model.browse(ids) or model.search(
            domain, offset=0, limit=False, order=False
        )

        if not model._is_an_ordinary_table():
            fields_name = [field for field in fields_name if field["name"] != "id"]

        field_names = [f["name"] for f in fields_name]
        #  FIXME: reference to raw data in odoo.export_data is still present, although variable has been removed.
        import_data = records.export_data(field_names).get("datas", [])

        if import_compat:
            columns_headers = field_names
        else:
            columns_headers = [val["label"].strip() for val in fields_name]

        if export_format == "csv":
            csv = CSVExport()
            return csv.from_data(columns_headers, import_data)
        else:
            xls = ExcelExport()
            return xls.from_data(columns_headers, import_data)

    @api.model
    # @Job
    def export(self, params):
        content = self._get_file_content(params)

        model_name, context, export_format = operator.itemgetter(
            "model", "context", "format"
        )(params)
        uid = context.get("uid") or params['uid'] or self.env.uid
        if not uid:
            raise UserError(_("No UID available. Cannot create export record."))
        # user = self.env["res.users"].browse([uid])

        export_record = self.sudo().create({"user_id": uid})
        name = "{}.{}".format(model_name, export_format.replace('excel', 'xlsx'))
        attachment = self.env["ir.attachment"].create(
            {
                "name": name,
                "datas": base64.b64encode(content),
                # "datas_fname": name,
                "type": "binary",
                "res_model": self._name,
                "res_id": export_record.id,
            }
        )

        # url = "{}/web/content/ir.attachment/{}/datas/{}?download=true".format(
        #     self.env["ir.config_parameter"].sudo().get_param("web.base.url"),
        #     attachment.id,
        #     attachment.name,
        # )

        time_to_live = (
            self.env["ir.config_parameter"].sudo().get_param("attachment.ttl", 7)
        )
        date_today = fields.Date.today()
        expiration_date = fields.Date.to_string(
            date_today + relativedelta(days=+int(time_to_live))
        )

        # TODO : move to email template
        email_from = params['email_from'] or self.sudo().env.ref("base.partner_root").email
        model_description = self.env[model_name]._description
        # email_to_list = []
        # if params['user_ids'] :
        #     for user in self.env["res.users"].browse(params['user_ids']):
        #         email_to_list.append(user.email)
        # else:
        #     email_to_list.append(user.email)
        # [tools.formataddr((partner.name or 'False', partner.email or 'False'))]
        auto_mail = "" if params['enable_reply'] else """
                <p>&nbsp;</p>
                <p><span style="color: #808080;">
                This is an automated message please do not reply.
                </span></p>"""
        self.env["mail.mail"].create(
            {
                "email_from": email_from,
                "reply_to": email_from if params['enable_reply'] else self.sudo().env.ref("base.partner_root").email,
                "email_to": params['email_to'] or False,
                "recipient_ids": params['partner_ids'] or False,
                "subject": _("{} {}").format(
                    params['subject'] if params['subject'] else f"Export {model_description}", fields.Date.to_string(fields.Date.today())
                ),
                "body_html": _(
                    """
                <p>Your export is available in the attachment.</p>  
                {}
                """
                ).format(auto_mail),
                "attachment_ids": [attachment.id],
                "auto_delete": True,
            }
        )

    @api.model
    def cron_delete(self):
        time_to_live = (
            self.env["ir.config_parameter"].sudo().get_param("attachment.ttl", 7)
        )
        date_today = fields.Date.today()
        date_to_delete = date_today + relativedelta(days=-int(time_to_live))
        self.search([("create_date", "<=", date_to_delete)]).unlink()

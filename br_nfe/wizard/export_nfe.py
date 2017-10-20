# -*- coding: utf-8 -*-
# © 2016 Alessandro Martini <alessandrofmartini@gmail.com>, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import io
import base64
# from datetime import date
import os.path
# from jinja2 import Environment, FileSystemLoader
from zipfile import ZipFile
from StringIO import StringIO
from odoo import api, fields, models


class ExportNfe(models.TransientModel):
    _name = 'wizard.export.nfe'

    start_date = fields.Date(string=u"Data Inicial", required=True)
    end_date = fields.Date(string=u"Data Final", required=True)
    model = fields.Many2one(
        'br_account.fiscal.document', string='Documento')
    name = fields.Char('Nome', size=255)
    file = fields.Binary('Arquivo', readonly=True)
    state = fields.Selection(
        [('init', 'init'), ('done', 'done')],
        'state', readonly=True, default='init')

    def _save_zip(self, xmls):
        tmp = '/tmp/odoo/nfse-export/'

        try:
            os.makedirs(tmp)
        except:
            pass
        zip_base64 = StringIO()
        zip_file = ZipFile(zip_base64, 'w')
        for xml in xmls:
            filename = os.path.join(tmp, xml['name'])
            with io.open(filename, 'w', encoding='utf8') as xml_file:
                xml_file.write(xml['content'])
            zip_file.write(filename, xml['name'])
        zip_file.close()
        zip_base64.seek(0)
        return base64.b64encode(zip_base64.getvalue())

    @api.multi
    def nfse_export(self):
        self.state = 'done'
        search_vals = []
        search_vals.append(('data_emissao', '>=', self.start_date))
        search_vals.append(('data_emissao', '<=', self.end_date))
        search_vals.append(('state', 'in', ['cancel', 'done', 'denied']))

        if self.model:
            search_vals.append(('model', 'in', [self.model.code]))

        invoice_ids = self.env['invoice.eletronic'].search(search_vals)
        xmls = []
        for invoice in invoice_ids:
            if not invoice.nfe_processada:
                invoice.generate_nfe_proc()
            xmls.append(base64.decodestring(invoice.nfe_processada))

        self.file = self._save_zip(xmls)
        self.name = 'xml_nfse_exportacao.zip'

        mod_obj = self.env['ir.model.data'].search(
            [('model', '=', 'ir.ui.view'),
             ('name', '=',
              'view_wizard_export_nfe')])

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(mod_obj.res_id, 'form')],
            'target': 'new',
        }

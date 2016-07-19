# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2016 TrustCode - www.trustcode.com.br                         #
#              Danimar Ribeiro <danimaribeiro@gmail.com>                      #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                             #
###############################################################################


from openerp import api, fields, models


class InvoiceEletronic(models.Model):
    _name = 'invoice.eletronic'

    code = fields.Char(u'Código', size=100)
    name = fields.Char(u'Name', size=100)
    company_id = fields.Many2one('res.company', u'Company', select=True)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
                             string=u'State', default='draft')

    tipo_operacao = fields.Selection([('entrada', 'Entrada'),
                                      ('saida', 'Saída')], u'Tipo emissão')
    model = fields.Selection([('55', 'NFe'), ('65', 'NFCe')], u'Modelo')
    serie = fields.Many2one('l10n_br_account.document.serie', string=u'Série')
    numero = fields.Integer(u'Número')
    numero_controle = fields.Integer(u'Número de Controle')
    data_emissao = fields.Datetime(u'Data emissão')
    data_fatura = fields.Datetime(u'Data Entrada/Saída')
    data_autorizacao = fields.Datetime(u'Data de autorização')

    ambiente = fields.Selection([('homologacao', 'Homologação'),
                                 ('producao', 'Produção')], u'Ambiente')
    finalidade_emissao = fields.Selection([('1', 'Normal'),
                                           ('2', 'Complementar'),
                                           ('3', 'Ajuste'),
                                           ('4', 'Devolução')],
                                          u'Finalidade da emissão')
    consumidor_final = fields.Selection([('0', 'Normal'),
                                         ('1', 'Consumidor')],
                                        u'Indicador de Consumidor Final')

    partner_id = fields.Many2one('res.partner', u'Parceiro')
    invoice_partner_id = fields.Many2one('res.partner', u'Faturamento')
    shipping_partner_id = fields.Many2one('res.partner', u'Entrega')
    payment_id = fields.Many2one('account.payment.term',
                                 string=u'Forma pagamento')
    fiscal_position_id = fields.Many2one('account.fiscal.position',
                                         string=u'Posição Fiscal')

    # parcela_ids = fields.One2many('sped.documentoduplicata',
    #  'documento_id', u'Vencimentos'),

    eletronic_item_ids = fields.One2many('invoice.eletronic.item',
                                         'invoice_eletronic_id',
                                         string=u"Linhas")

    total_tax_icms_id = fields.Many2one('sped.tax.icms', string=u'Total ICMS')
    total_tax_ipi_id = fields.Many2one('sped.tax.ipi', string=u'Total IPI')
    total_tax_ii_id = fields.Many2one('sped.tax.ii',
                                      string=u'Total Imposto de importação')
    total_tax_pis_id = fields.Many2one('sped.tax.pis', string=u'Total PIS')
    total_tax_cofins_id = fields.Many2one('sped.tax.cofins',
                                          string=u'Total Cofins')
    total_tax_issqn_id = fields.Many2one('sped.tax.issqn',
                                         string=u'Total ISSQN')
    total_tax_csll_id = fields.Many2one('sped.tax.csll',
                                        string=u'Total CSLL')
    total_tax_irrf_id = fields.Many2one('sped.tax.irrf', string=u'Total IRRF')
    total_tax_inss_id = fields.Many2one('sped.tax.inss', string=u'Total INSS')

    valor_bruto = fields.Float(u'Valor Produtos')
    valor_frete = fields.Float(u'Valor do frete')
    valor_seguro = fields.Float(u'Valor do seguro')
    valor_desconto = fields.Float(u'Valor do desconto')
    valor_despesas = fields.Float(u'Valor despesas')
    valor_retencoes = fields.Float(u'Retenções')

    valor_final = fields.Float(u'Valor Final')

    transportation_id = fields.Many2one('invoice.transport')

    informacoes_legais = fields.Text(u'Informações legais')
    informacoes_complementar = fields.Text(u'Informações complementares')

    @api.multi
    def _prepare_eletronic_invoice_values(self):
        return {}

    @api.multi
    def action_send_eletronic_invoice(self):
        pass

class InvoiceEletronicItem(models.Model):
    _name = 'invoice.eletronic.item'

    name = fields.Char(u'Nome', size=100)
    company_id = fields.Many2one('res.company', u'Empresa', select=True)
    invoice_eletronic_id = fields.Many2one('invoice.eletronic', u'Documento')

    product_id = fields.Many2one('product.product', string=u'Produto')
    cfop = fields.Char(u'CFOP', size=5)

    uom_id = fields.Many2one('produt.uom', u'Unidade de medida')
    quantity = fields.Float(u'Quantidade')
    unit_price = fields.Float(u'Preço Unitário')

    freight_value = fields.Float(u'Frete')
    insurance_value = fields.Float(u'Seguro')
    discount = fields.Float(u'Desconto')
    other_expenses = fields.Float(u'Outras despesas')

    gross_total = fields.Float(u'Valor Bruto')
    total = fields.Float(u'Valor Liquido')

    tax_icms_id = fields.Many2one('sped.tax.icms', string=u'ICMS')
    tax_ipi_id = fields.Many2one('sped.tax.ipi', string=u'IPI')
    tax_ii_id = fields.Many2one('sped.tax.ii', string=u'Imposto de importação')
    tax_pis_id = fields.Many2one('sped.tax.pis', string=u'PIS')
    tax_cofins_id = fields.Many2one('sped.tax.cofins', string=u'Cofins')
    tax_issqn_id = fields.Many2one('sped.tax.issqn', string=u'ISSQN')
    tax_csll_id = fields.Many2one('sped.tax.csll', string=u'CSLL')
    tax_irrf_id = fields.Many2one('sped.tax.irrf', string=u'IRRF')
    tax_inss_id = fields.Many2one('sped.tax.inss', string=u'INSS')


class InvoiceTransport(models.Model):
    _name = 'invoice.transport'

    name = fields.Char(u'Nome', size=100)
    company_id = fields.Many2one('res.company', u'Empresa', select=True)

    modalidade_frete = fields.Selection([('0', 'Sem Frete'),
                                         ('1', 'Por conta do destinatário'),
                                         ('2', 'Por conta do emitente'),
                                         ('9', 'Outros')],
                                        u'Modalidade do frete')
    transportadora_id = fields.Many2one('res.partner', u'Transportadora')
    placa_veiculo = fields.Char('Placa do Veiculo', size=7)
    estado_veiculo_id = fields.Many2one('res.country.state', 'UF da Placa')
    cidade_veiculo_id = fields.Many2one(
        'l10n_br_base.city', 'Municipio',
        domain="[('state_id', '=', estado_veiculo_id)]")
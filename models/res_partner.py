from odoo import models, fields, api


class Client(models.Model):
    _inherit = "res.partner"

    reservation_ids = fields.One2many(comodel_name='alldons.resv', inverse_name='client_id')
    partner_resv = fields.Many2one(related='reservation_ids.client_id')


class alldonsEmp(models.Model):
    _name = 'alldons.emp'

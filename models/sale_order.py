from AptUrl.Helpers import _
from odoo import models,fields, api

class Quotation(models.Model):
    _inherit = "sale.order"

    reservation_ids = fields.One2many(comodel_name='alldons.resv', inverse_name='devis')
    nbr_reservation = fields.Integer(string="compute reservation",compute='_compute_nbr_reservation')
    create_after_resv = fields.Boolean(default=False)

    def _compute_nbr_reservation(self):
        self.nbr_reservation=len(self.reservation_ids.ids)


    def show_reservation(self):
        return {
            'name': 'Reservation',
            'type': 'ir.actions.act_window',
            'res_model': 'alldons.resv',
            'view_mode': 'tree,form',
            'domain': [('id','in', self.reservation_ids.ids)]

        }
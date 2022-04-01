# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api
from stdnum.exceptions import ValidationError


class Reservation(models.Model):
    _name = 'alldons.resv'
    titre = fields.Char('titre')
    description = fields.Char('description')
    date_res = fields.Datetime('date de reservation')
    client_id = fields.Many2one(comodel_name='res.partner')
    article_ids = fields.Many2many(comodel_name='product.template', relation='article_resv', column1='titre',
                                   column2='name')
    state = fields.Selection([('l1', 'New'), ('l2', 'confirm'), ('l3', 'done'), ('l4', 'cancel')], default='l1')
    duree_resv_month = fields.Integer('durée_month')
    duree_resv_day = fields.Integer('durée_day')
    duree_resv_hour = fields.Integer('durée_hour')
    fin_reservation = fields.Datetime(string='fin reservation', compute='_compute_end_reservation')
    devis = fields.Many2one(comodel_name='sale.order')
    partner = fields.Many2one(related='devis.partner_id')
    ref = fields.Char(String="reference", required=True, copy=False, readonly=True, default='/')
    nbr_hour = fields.Integer('nbr_hour',compute='_nbr_hour_reservation',store=True)



    def action_confirm(self):
        self.state = 'l2'


    def action_done(self):
        self.state = 'l3'

    def action_cancel(self):
        self.state = 'l4'

    def action_new(self):
        self.state = 'l1'

    def action_quotation(self):
        users = set(self.client_id)
        price = 0
        for user in users:
            reserve = [record for record in self if record.client_id == user]
            value = self.env['sale.order'].create({'partner_id': user.id,'create_after_resv':True})
            for res in reserve:
                if res.state == 'l3':
                    if res.duree_resv_hour < 10:
                        price = 150

                    else:
                        price = 140

                        value.create_date = datetime.date.today()

                        value.reservation_ids = [

                            (0, 0, {
                                'ref': res.ref,
                                'titre': res.titre,
                                'description': res.description,
                                'date_res': res.date_res,

                                'duree_resv_month': res.duree_resv_month,
                                'duree_resv_day': res.duree_resv_day,
                                'duree_resv_hour': res.duree_resv_hour,
                                'fin_reservation': res.fin_reservation,
                                'client_id': res.client_id.id,
                                'state': res.state,

                            })]

                        value.order_line = [

                            (0, 0, {
                                'price_unit': price,
                                'product_uom_qty': res.duree_resv_hour,
                                'product_id': res.article_ids.id,
                                'name': res.article_ids.name
                            })]

                    res.devis = value



                else:
                    raise ValidationError('vous ne pouvez pas créer un devis non valide')

    # from odoo import models, fields, api

    # class alldons(models.Model):
    # _name = 'alldons.alldons'
    #  _description = 'alldons.alldons'

    # name = fields.Char()
    # value = fields.Integer()
    # value2 = fields.Float(compute="_value_pc", store=True)
    # description = fields.Text()

    # @api.depends('value')
    # def _value_pc(self):
    # for record in self:
    #   record.value2 = float(record.value) / 100
    # @api.multi
    # def name_get(self):
    # result = []
    # for reservation in self:
    # name='['+ reservation.emp_id.nom + ']' + reservation.titre
    # result.append((reservation.id,reservation.name))
    #  return result

    @api.model
    def create(self, vals):
        if vals.get('ref', '/') == '/':
            vals['ref'] = self.env['ir.sequence'].next_by_code('reservation.sequence') or '/'
        res = super(Reservation, self).create(vals)
        return res

    def _compute_end_reservation(self):
        for s in self:
            somme_day = s.duree_resv_day + s.duree_resv_month * 30

            somm_heure = s.duree_resv_hour * 3600
            t_delta = datetime.timedelta(days=somme_day, seconds=somm_heure)
            s.fin_reservation = s.date_res + t_delta


    def _nbr_hour_reservation(self):
        for rec in self:
            rec.nbr_hour = rec.duree_resv_hour+rec.duree_resv_day*24+rec.duree_resv_month*30*24


        print(self.nbr_hour)
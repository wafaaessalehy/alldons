
from odoo import api, http, models
from odoo.http import request



class Alldons(http.Controller):
   @http.route('/get_reservation', auth='public',type="json",csrf=False)
   def get_reservation(self):
       reservation_rec = request.env['alldons.resv'].search([])
       reservation =[]
       for rec in reservation_rec:
           val = {

               'titre':rec.titre,
               'description':rec.description,

           }
           reservation.append(val)
       print(reservation)
       data={'status':200,'response':reservation,'message':'Success'}
#

#     @http.route('/alldons/alldons/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('alldons.listing', {
#             'root': '/alldons/alldons',
#             'objects': http.request.env['alldons.alldons'].search([]),
#         })

#     @http.route('/alldons/alldons/objects/<model("alldons.alldons"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('alldons.object', {
#             'object': obj
#         })

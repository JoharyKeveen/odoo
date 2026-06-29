from odoo import models, fields, api

class CrmVip(models.Model):
    _name = 'crm.vip'
    _description = 'Client VIP'

    name = fields.Char(string='Nom du client', required=True)
    email = fields.Char(string='Email')
    telephone = fields.Char(string='Téléphone')
    niveau_vip = fields.Selection([
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ], string='Niveau VIP', default='bronze')
    chiffre_affaires = fields.Float(string="Chiffre d'affaires")
    date_adhesion = fields.Date(string="Date d'adhésion")
    actif = fields.Boolean(string='Actif', default=True)
    notes = fields.Text(string='Notes')
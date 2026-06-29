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

    opportunite_ids = fields.One2many(
    comodel_name='crm.lead',
    inverse_name='vip_id',
    string='Opportunités',
    )

     # Champ calculé
    categorie = fields.Char(
        string='Catégorie automatique',
        compute='_compute_categorie',
        store=True
    )

    @api.depends('chiffre_affaires')
    def _compute_categorie(self):
        for rec in self:
            if rec.chiffre_affaires < 10000:
                rec.categorie = 'Bronze'
            elif rec.chiffre_affaires < 50000:
                rec.categorie = 'Silver'
            elif rec.chiffre_affaires < 100000:
                rec.categorie = 'Gold'
            else:
                rec.categorie = 'Platinum'
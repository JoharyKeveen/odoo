from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class CrmVip(models.Model):
    _name = 'crm.vip'
    _description = 'Client VIP'
    _inherit = ['mail.thread', 'mail.activity.mixin']

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

    @api.constrains('chiffre_affaires')
    def _check_chiffre_affaires(self):
        for rec in self:
            if rec.chiffre_affaires < 0:
                raise ValidationError(
                    "Le chiffre d'affaires ne peut pas être négatif."
                )

    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if rec.email and '@' not in rec.email:
                raise ValidationError(
                    "L'adresse email saisie n'est pas valide (il manque le @)."
                )

    @api.constrains('date_adhesion')
    def _check_date_adhesion(self):
        for rec in self:
            if rec.date_adhesion and rec.date_adhesion > date.today():
                raise ValidationError(
                    "La date d'adhésion ne peut pas être dans le futur."
                )
            
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('chiffre_affaires', 0) > 100000:
                vals['niveau_vip'] = 'platinum'
        return super().create(vals_list)

    def write(self, vals):
        if 'chiffre_affaires' in vals and vals['chiffre_affaires'] > 100000:
            vals['niveau_vip'] = 'platinum'
        return super().write(vals)
    
    def action_envoyer_email_bienvenue(self):
        for rec in self:
            if not rec.email:
                raise ValidationError(
                    "Impossible d'envoyer un email : ce client n'a pas d'adresse email."
                )
            rec.message_post(
                body=f"Email de bienvenue envoyé à {rec.name} ({rec.email})"
            )
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Succès',
                'message': 'Email de bienvenue envoyé avec succès !',
                'type': 'success',
                'sticky': False,
            }
        }
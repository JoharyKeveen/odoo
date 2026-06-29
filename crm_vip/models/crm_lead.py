from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    vip_id = fields.Many2one(
        comodel_name='crm.vip',
        string='Client VIP',
        ondelete='set null',
    )
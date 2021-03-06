# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.tools.float_utils import float_round
from odoo.http import request

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    inventory_availability = fields.Selection([
        ('never', 'Sell regardless of inventory'),
        ('always', 'Show inventory on website and prevent sales if not enough stock'),
        ('threshold', 'Show inventory below a threshold and prevent sales if not enough stock'),
        ('custom', 'Show product-specific notifications'),
    ], string='Inventory Availability', help='Adds an inventory availability status on the web product page.', default='never')
    available_threshold = fields.Float(string='Availability Threshold', default=5.0)
    custom_message = fields.Text(string='Custom Message', default='')

    def _compute_quantities(self):
        website = request and getattr(request, 'website', None)

        if not website:
            super(ProductTemplate, self)._compute_quantities()
        else:

            res = self._compute_quantities_dict()
            for template in self:
                rounding = template.uom_id.rounding
                template.qty_available = res[template.id]['qty_available']
                template.virtual_available = float_round(
                    res[template.id]['qty_available'] - res[template.id]['outgoing_qty'], rounding)
                template.incoming_qty = res[template.id]['incoming_qty']
                template.outgoing_qty = res[template.id]['outgoing_qty']
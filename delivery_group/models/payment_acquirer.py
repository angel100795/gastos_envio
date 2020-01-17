# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    only_published_for_group_ids = fields.Many2many(
        'res.groups',
        'delivery_carrier_group_rel',
        'carrier_id', 'group_id',
        string='Only Published for Groups',
        help='Set which groups are allowed to use this payment acquirer. If no'
        ' group specified this payment option will be available for everybody'
    )


    # no pudimos hacerlo andar con la nueva api!
    def website_publish_button(
        self, cr, uid, ids, context=None):
        """
        We can not use security because the render of button in website is
        called with superuser
        TODO: not sure why it dont works in new api
        NOTA: este metodo no devuelve lo permitido por el usuario logueado
        si no mas bien lo relativo al partner, por ej, viendo una orden de
        venta, por mas que sea super admin, solo veo segun permiso del
        partner de la orden de venta
        """
        carrier = self.browse(cr, uid, id)
        if carrier.only_published_for_group_ids:
            # check if there is a match between users and groups required
            groups_ids = self.pool['res.groups'].search(cr, uid, [
                ('users', 'in', user_ids),
                ('id', 'in', carrier.only_published_for_group_ids.ids)],
                context=context)
            print (groups_ids)
            if not groups_ids:
                return False
        return super(DeliveryCarrier, self).website_publish_button(
            cr, uid, ids, context=None)

from odoo.tests.common import TransactionCase


class TestBook(TransactionCase):

    def setup(self, *args, **kwargs):
        result = super().setup(*args, **kwargs)
        self.Product_template = self.env['product.template']
        self.product_template_ode = self.Product_template.create({
            'name': 'Base prod 1',
            'qty_available': '5',
            'produced_units': '4'})
        # TODO: Add parent element to check that tau calcs properly, qty_available = 3,
        # TODO: Add child elements to check that tau calcs properly, qty_available = 7, 'produced_units': '2',
        #       qty_available = 9, 'produced_units': '6',
        return result

    def test_base_tau_eq_qty_available(self):
        """Test Product template base TAU = Stock on hand"""
        self.assertEqual(self.product_template_ode.parent_pack_id.total_available_units,
                         self.product_template_ode.parent_pack_id.qty_available)

    def test_base_tau_eq_child_tau_totals(self):
        """Test Product templates calculate correctly"""
        self.assertEqual(self.parent_pack_id.total_available_units, 3)

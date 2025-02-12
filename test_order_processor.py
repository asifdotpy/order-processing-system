import unittest
from order_processor import calculate_order_total, load_orders, process_orders
import json
import os

class TestOrderProcessor(unittest.TestCase):
    def setUp(self):
        # Basic valid orders for testing
        self.test_orders = [
            {
                "order_id": 101,
                "customer": "Alice",
                "items": [
                    {"name": "Laptop", "price": 1000, "quantity": 1},
                    {"name": "Mouse", "price": 50, "quantity": 2}
                ],
                "discount_code": "SUMMER10"
            },
            {
                "order_id": 102,
                "customer": "Bob",
                "items": [
                    {"name": "Monitor", "price": 200, "quantity": 2}
                ],
                "discount_code": None
            }
        ]
        self.discounts = {"SUMMER10": 10, "WELCOME5": 5}
        self.test_file = 'test_orders.json'
        with open(self.test_file, 'w') as f:
            json.dump(self.test_orders, f)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_load_orders(self):
        orders = load_orders(self.test_file)
        self.assertEqual(len(orders), 2)
        self.assertEqual(orders[0]['order_id'], 101)

    def test_calculate_order_total_valid(self):
        order = self.test_orders[0]
        result = calculate_order_total(order, self.discounts)
        expected_total_before = 1000 + 50 * 2
        expected_total_after = expected_total_before * 0.9  # 10% discount
        self.assertEqual(result['total_before'], expected_total_before)
        self.assertEqual(result['total_after'], expected_total_after)

    def test_calculate_order_total_invalid_discount(self):
        # Order with no discount should simply have total_after equal to total_before.
        order = self.test_orders[1]
        result = calculate_order_total(order, self.discounts)
        expected_total = 200 * 2
        self.assertEqual(result['total_after'], expected_total)

    def test_process_orders(self):
        processed = process_orders(self.test_orders, self.discounts)
        self.assertEqual(len(processed), 2)
        self.assertEqual(processed[0]['order_id'], 101)
        
    # Additional Test Cases for Edge Conditions:

    def test_missing_order_id(self):
        # Order missing 'order_id' should return None.
        order = {
            "customer": "Charlie",
            "items": [
                {"name": "Keyboard", "price": 100, "quantity": 1}
            ],
            "discount_code": "WELCOME5"
        }
        result = calculate_order_total(order, self.discounts)
        self.assertIsNone(result)

    def test_missing_customer(self):
        # Order missing 'customer' should return None.
        order = {
            "order_id": 103,
            "items": [
                {"name": "Keyboard", "price": 100, "quantity": 1}
            ],
            "discount_code": "WELCOME5"
        }
        result = calculate_order_total(order, self.discounts)
        self.assertIsNone(result)
        
    def test_invalid_items_type(self):
        # When 'items' is not a list, the function should return None.
        order = {
            "order_id": 104,
            "customer": "Diana",
            "items": "Not a list",
            "discount_code": "WELCOME5"
        }
        result = calculate_order_total(order, self.discounts)
        self.assertIsNone(result)
        
    def test_negative_price_or_quantity(self):
        # Items with negative price or quantity should be skipped.
        order = {
            "order_id": 105,
            "customer": "Eve",
            "items": [
                {"name": "Monitor", "price": -200, "quantity": 2},  # Invalid
                {"name": "Mouse", "price": 50, "quantity": -1},       # Invalid
                {"name": "Keyboard", "price": 100, "quantity": 1}       # Valid
            ],
            "discount_code": None
        }
        result = calculate_order_total(order, self.discounts)
        # Only the valid item ("Keyboard") should count.
        self.assertAlmostEqual(result['total_before'], 100)
        self.assertAlmostEqual(result['total_after'], 100)
        
    def test_invalid_discount_code(self):
        # Discount code that is not in the discount dictionary should be treated as 0% discount.
        order = {
            "order_id": 106,
            "customer": "Frank",
            "items": [
                {"name": "Laptop", "price": 1200, "quantity": 1}
            ],
            "discount_code": "INVALID_CODE"
        }
        result = calculate_order_total(order, self.discounts)
        self.assertAlmostEqual(result['total_before'], 1200)
        self.assertAlmostEqual(result['total_after'], 1200)
        
    def test_item_missing_fields(self):
        # If an item is missing required fields, it should be skipped.
        order = {
            "order_id": 107,
            "customer": "Grace",
            "items": [
                {"name": "Tablet", "price": 300, "quantity": 1},
                {"name": "Case", "quantity": 2}  # Missing 'price'
            ],
            "discount_code": "WELCOME5"
        }
        result = calculate_order_total(order, self.discounts)
        # Only the valid item (Tablet) should be counted.
        self.assertAlmostEqual(result['total_before'], 300)
        self.assertAlmostEqual(result['total_after'], 300 * 0.95)

if __name__ == '__main__':
    unittest.main()


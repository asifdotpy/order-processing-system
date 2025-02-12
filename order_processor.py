import json
import logging
import argparse
from concurrent.futures import ThreadPoolExecutor

# Try to import tqdm for progress indication
try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

# Configure logging once; default level is INFO, can be overridden via CLI arguments.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DISCOUNTS = {"SUMMER10": 10, "WELCOME5": 5}

def load_orders(file_path):
    """Load orders from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list: A list of order dictionaries.

    Raises:
        FileNotFoundError, json.JSONDecodeError: When file issues occur.
    """
    try:
        with open(file_path, 'r') as f:
            orders = json.load(f)
            return orders  # orders is a list of order dicts
    except FileNotFoundError:
        logging.error("File not found: %s", file_path)
        raise
    except json.JSONDecodeError as e:
        logging.error("Invalid JSON in file %s: %s", file_path, e)
        raise
    except Exception as e:
        logging.error("Error loading orders: %s", e)
        raise

def calculate_order_total(order, discounts):
    """Calculate total before and after discount for an order.

    Args:
        order (dict): Order information.
        discounts (dict): Mapping of discount codes to percentage discount.

    Returns:
        dict or None: Processed order with totals, or None if the order is invalid.
    """
    order_id = order.get('order_id')
    if order_id is None:
        logging.error("Order missing 'order_id'")
        return None

    customer = order.get('customer')
    if customer is None:
        logging.error("Order %s missing 'customer'", order_id)
        return None

    items = order.get('items', [])
    if not isinstance(items, list):
        logging.error("Order %s has invalid items list", order_id)
        return None

    total_before = 0.0
    for item in items:
        name = item.get('name')
        price = item.get('price')
        quantity = item.get('quantity')
        if None in (name, price, quantity):
            logging.warning("Item in order %s missing name, price or quantity", order_id)
            continue
        try:
            price = float(price)
            quantity = int(quantity)
        except (TypeError, ValueError):
            logging.error("Invalid price or quantity in order %s", order_id)
            continue
        if price < 0 or quantity < 0:
            logging.error("Negative price or quantity in order %s", order_id)
            continue
        total_before += price * quantity

    discount_code = order.get('discount_code')
    discount_percent = discounts.get(discount_code, 0) if discount_code else 0
    total_after = total_before * (1 - discount_percent / 100)

    return {
        'order_id': order_id,
        'customer': customer,
        'total_before': round(total_before, 2),
        'total_after': round(total_after, 2)
    }

def process_orders(orders, discounts, show_progress=False):
    """Process orders in parallel using ThreadPoolExecutor.

    Args:
        orders (list): List of order dictionaries.
        discounts (dict): Discount mapping.
        show_progress (bool): Whether to display a progress bar.

    Returns:
        list: List of successfully processed orders.
    """
    with ThreadPoolExecutor() as executor:
        if show_progress and tqdm:
            processed_orders = list(tqdm(executor.map(lambda order: calculate_order_total(order, discounts), orders),
                                         total=len(orders)))
        else:
            processed_orders = list(executor.map(lambda order: calculate_order_total(order, discounts), orders))
    valid_orders = [order for order in processed_orders if order is not None]
    skipped = len(orders) - len(valid_orders)
    if skipped:
        logging.info("Skipped %d orders due to errors.", skipped)
    return valid_orders

def generate_report(processed_orders, output_file):
    """Generate the invoice summary report.

    Args:
        processed_orders (list): List of processed order dictionaries.
        output_file (str): Path to the output file.
    """
    try:
        with open(output_file, 'w') as f:
            for order in processed_orders:
                line = (
                    f"Order ID: {order['order_id']} | Customer: {order['customer']} | "
                    f"Total Before Discount: ${order['total_before']:.2f} | "
                    f"Total After Discount: ${order['total_after']:.2f}\n"
                )
                f.write(line)
    except IOError as e:
        logging.error("Error writing to report file: %s", e)
        raise

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Process orders and generate an invoice summary.")
    parser.add_argument('--input', default='orders.json', help='Path to the orders JSON file.')
    parser.add_argument('--output', default='invoice_summary.txt', help='Path to the output report file.')
    parser.add_argument('--progress', action='store_true', help='Show progress bar during processing.')
    parser.add_argument('--log', default='INFO', help='Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).')
    return parser.parse_args()

def main():
    args = parse_args()

    # Set logging level from command-line argument
    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        logging.error("Invalid log level: %s", args.log)
        numeric_level = logging.INFO
    logging.getLogger().setLevel(numeric_level)

    logging.info("Starting order processing...")
    orders = load_orders(args.input)
    logging.info("Loaded %d orders from %s", len(orders), args.input)

    processed_orders = process_orders(orders, DISCOUNTS, show_progress=args.progress)
    logging.info("Processed %d orders", len(processed_orders))

    generate_report(processed_orders, args.output)
    logging.info("Report generated successfully at %s", args.output)

    # Print the content of the report
    try:
        with open(args.output, 'r') as f:
            print("\nInvoice Summary:")
            print(f.read())
    except Exception as e:
        logging.error("Error reading the generated report: %s", e)

if __name__ == "__main__":
    main()


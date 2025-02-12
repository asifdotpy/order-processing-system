```markdown
# Order Processing System

A Python-based order processing system that calculates order totals, applies discounts, and generates invoice summaries.

## Features

- Load and process orders from JSON files
- Apply discount codes to orders
- Parallel processing of orders using `ThreadPoolExecutor`
- Optional progress bar support using `tqdm`
- Comprehensive error handling and logging with configurable levels
- Generate invoice summary reports with detailed order totals

## Requirements

- Python 3.6 or higher
- Standard library modules only; if you want a progress bar, install [`tqdm`](https://pypi.org/project/tqdm/) via pip:
  ```bash
  pip install tqdm
  ```

## Installation

1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Unix or macOS:
     ```bash
     source venv/bin/activate
     ```

## Usage

The system supports several command-line arguments to customize its behavior.

### Basic Usage

1. Ensure you have a valid `orders.json` file in the project directory (see below for the required format).
2. Run the script:
   ```bash
   python order_processor.py
   ```
   This uses the default input (`orders.json`), output (`invoice_summary.txt`), logging level (`INFO`), and no progress bar.

### Advanced Options

You can customize the execution using the following options:

- **Specify Input and Output Files:**
  ```bash
  python order_processor.py --input my_orders.json --output my_invoice.txt
  ```
- **Set Logging Level:**
  ```bash
  python order_processor.py --log DEBUG
  ```
- **Show Progress Bar (if `tqdm` is installed):**
  ```bash
  python order_processor.py --progress
  ```

## Input File Format

The `orders.json` file should contain a JSON array of order objects. Each order object must have the following structure:

```json
[
  {
    "order_id": 101,
    "customer": "Alice",
    "items": [
      {
        "name": "Laptop",
        "price": 1000,
        "quantity": 1
      },
      {
        "name": "Mouse",
        "price": 50,
        "quantity": 2
      }
    ],
    "discount_code": "SUMMER10"  // Optional: use null if no discount applies
  },
  {
    "order_id": 102,
    "customer": "Bob",
    "items": [
      {
        "name": "Monitor",
        "price": 200,
        "quantity": 2
      }
    ],
    "discount_code": null
  }
]
```

**Note:**  
- The file is simply an array (not wrapped in an object).
- Each item should have keys: `name`, `price`, and `quantity`.

## Available Discount Codes

- **SUMMER10:** 10% discount
- **WELCOME5:** 5% discount

Any discount code not listed will be treated as 0% discount.

## Output

The script generates an invoice summary report (default: `invoice_summary.txt`) containing:

- Order ID
- Customer name
- Total before discount
- Total after discount

Example output:

```
Order ID: 101 | Customer: Alice | Total Before Discount: $1100.00 | Total After Discount: $990.00
Order ID: 102 | Customer: Bob | Total Before Discount: $400.00 | Total After Discount: $400.00
```

## Error Handling & Logging

- The system logs errors and warnings with timestamps.
- Common issues include:
  - Missing or invalid JSON files.
  - Orders with missing required fields (`order_id`, `customer`, or `items`).
  - Items with invalid or negative price/quantity.
- Logging level can be adjusted via the `--log` command-line option.

## Testing

Unit tests are provided to ensure the system works as expected, including edge cases. Run the tests with:

```bash
python -m unittest discover
```

or

```bash
python test_order_processor.py
```

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes with clear messages.
4. Push your branch.
5. Create a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

---

This updated README now provides clear instructions for using the new command‑line options, explains the correct JSON input format, and gives developers all the necessary details about error handling, logging, and testing.

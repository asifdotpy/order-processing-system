# Automated Order Processing System

A Python-based system to process customer orders, apply discounts, and generate invoice summaries.

## Features

- Load orders from a JSON file
- Apply discounts using predefined codes
- Calculate totals before and after discounts
- Parallel order processing with `ThreadPoolExecutor`
- Error handling and logging
- Generate an invoice summary report

## Requirements

- **Python 3.6 or higher**
- No external dependencies required

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/order-processing-system.git
   ```
2. Navigate to the project directory:
   ```bash
   cd order-processing-system
   ```

## Usage

### Step 1: Prepare the Input File
- Create an `orders.json` file in the project root (see [Input Format](#input-format) for details).

### Step 2: Run the Processor
```bash
python order_processor.py
```
- This reads `orders.json` and generates `invoice_summary.txt` by default.

## Input Format

The `orders.json` file must contain an array of order objects. Example:
```json
[
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
    "discount_code": null
  }
]
```

**Notes**:
- `discount_code` is optional. Use `null` for no discount.
- Prices and quantities must be non-negative.

## Discount Codes
- `SUMMER10`: 10% discount
- `WELCOME5`: 5% discount  
*(Add more codes in the `DISCOUNTS` dictionary in `order_processor.py`)*

## Output

The system generates `invoice_summary.txt` with lines like:
```
Order ID: 101 | Customer: Alice | Total Before Discount: $1100.00 | Total After Discount: $990.00
Order ID: 102 | Customer: Bob | Total Before Discount: $400.00 | Total After Discount: $400.00
```

## Error Handling
- Logs errors to the console (e.g., invalid JSON, missing fields).
- Skips orders with critical issues (e.g., negative prices).

## Testing
Run unit tests with:
```bash
python test_order_processor.py
```

## License
MIT License. See [LICENSE](LICENSE) for details.
```

### Key Changes:
1. **Removed Unsupported Features**:  
   - Deleted references to `tqdm`, progress bars, and CLI arguments (not in the code).
   - Simplified the "Features" section to match the actual implementation.

2. **Streamlined Instructions**:  
   - Removed virtual environment setup (optional for a README).
   - Focused on core usage steps.

3. **Alignment with Code**:  
   - Removed mentions of configurable logging levels (code uses fixed `ERROR` logging).
   - Clarified that `orders.json` and `invoice_summary.txt` are hardcoded.

4. **Formatting Improvements**:  
   - Simplified sections for readability.
   - Added a direct example for running tests.  

This version ensures the README accurately reflects the provided code and avoids misleading users. 🚀

# 📤 FraudAGENT - Excel Upload Feature

## Overview

The **Excel Upload Feature** allows you to use your own insurance data with FraudAGENT. Simply upload an Excel file (.xlsx) and the system will automatically convert it to Parquet format and use it as the primary data source for all predictions and analysis.

## Quick Start

1. **Launch the application**
   ```bash
   python3 main_with_upload.py
   ```

2. **Open the web interface** at http://localhost:7860

3. **Navigate to the "Data Upload" tab**

4. **Upload your Excel file** (.xlsx format)

5. **Click "Convert to Parquet"**

6. **Restart the application** to use your new data

## What Gets Converted

The system converts your Excel file as follows:

- **Each sheet** → Separate Parquet table
- **Column headers** → Table columns
- **Data types** → Automatically detected
- **Primary keys** → Auto-detected (ID columns)
- **Foreign keys** → Auto-detected (reference columns)
- **Temporal columns** → Auto-detected (date/time columns)
- **Relationships** → Auto-inferred between tables

## Example Excel Structure

### Sheet 1: customers
| customer_ID | name | birth_date | state |
|-------------|------|------------|-------|
| CUST001 | John Doe | 1985-05-10 | CA |
| CUST002 | Jane Smith | 1990-08-15 | NY |

### Sheet 2: claims
| claim_ID | customer_ID | claim_date | amount | fraud_flag |
|----------|-------------|------------|--------|------------|
| CLM001 | CUST001 | 2024-01-15 | 1500.00 | False |
| CLM002 | CUST002 | 2024-02-20 | 3200.00 | True |

The system will automatically detect that `customer_ID` in the `claims` sheet references `customer_ID` in the `customers` sheet.

## Files Created

After conversion, the following files are created in `uploaded_data/`:

```
uploaded_data/
├── customers.parquet
├── claims.parquet
├── policies.parquet
├── ...
└── upload_metadata.json
```

## Data Source Priority

The application loads data in this order:

1. **uploaded_data/** (if exists) ← Your uploaded data
2. **INSURANCE_DATA_PATH** (from .env)
3. **data/** (default sample data)

## Technical Details

### Conversion Process

1. **Read Excel** - All sheets are read into memory
2. **Schema Detection** - Analyze columns, types, keys
3. **Relationship Inference** - Detect foreign key relationships
4. **Parquet Export** - Save each table as Parquet
5. **Metadata Export** - Save schema and relationships to JSON

### Supported Features

- ✅ Multiple sheets per Excel file
- ✅ Automatic data type detection
- ✅ Primary key detection
- ✅ Foreign key detection
- ✅ Temporal column detection
- ✅ Relationship inference
- ✅ Schema validation
- ✅ Metadata export

### Requirements

- Excel file must be `.xlsx` format
- First row must contain column headers
- ID columns should follow naming conventions (e.g., `customer_ID`, `claim_ID`)
- Date columns should be formatted as dates in Excel

## Troubleshooting

### "No relationships inferred"

**Solution**: Ensure foreign key columns have the same name as the primary key they reference.

Example:
- ✅ `claims.customer_ID` → `customers.customer_ID`
- ❌ `claims.cust_id` → `customers.customer_ID`

### "Conversion failed"

**Common causes**:
- Merged cells in Excel
- Missing headers
- Invalid data types
- Empty sheets

**Solution**: Clean your Excel file and ensure it follows the requirements.

### "Old data still being used"

**Solution**: You must restart the application after uploading new data.

## Advanced Usage

### Manual Conversion (CLI)

You can also convert Excel files manually using the command line:

```bash
python3 src/excel_converter.py /path/to/your/file.xlsx
```

This will create the `uploaded_data/` directory with all converted files.

### Programmatic Usage

```python
from src.excel_converter import ExcelToParquetConverter

# Create converter
converter = ExcelToParquetConverter(output_dir="uploaded_data")

# Convert Excel to Parquet
tables = converter.convert_excel_to_parquet("insurance_data.xlsx")

# Analyze schema
schema_info = converter.analyze_schema()

# Infer relationships
relationships = converter.infer_relationships()

# Export metadata
converter.export_metadata()

# Validate conversion
is_valid = converter.validate_conversion()
```

## See Also

- [UPLOAD_FEATURE_GUIDE.md](UPLOAD_FEATURE_GUIDE.md) - Detailed user guide
- [README.md](README.md) - Main application documentation
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Production deployment

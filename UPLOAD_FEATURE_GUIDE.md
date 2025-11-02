# FraudAGENT - Excel Data Upload Guide

This guide provides detailed instructions for using the **Excel Data Upload** feature in the FraudAGENT application. This powerful feature allows you to bring your own insurance data and use it as the primary source for KumoRFM graph creation and predictive analysis.

---

## 📋 Table of Contents

1.  [Feature Overview](#feature-overview)
2.  [How It Works](#how-it-works)
3.  [Excel File Requirements](#excel-file-requirements)
4.  [Step-by-Step Usage Guide](#step-by-step-usage-guide)
5.  [Technical Details](#technical-details)
6.  [Troubleshooting](#troubleshooting)

---

## Feature Overview

The Data Upload feature enables you to replace the default sample data with your own dataset by simply uploading a single Excel (`.xlsx`) file. The system automatically processes the file, converts it to a high-performance format (Parquet), and prepares it for analysis.

**Key Capabilities:**
-   **Bring Your Own Data (BYOD)**: Analyze your own insurance claims data.
-   **Automatic Conversion**: Converts all sheets in an Excel file to separate Parquet tables.
-   **Schema Inference**: Automatically detects data types, primary keys, foreign keys, and temporal columns.
-   **Relationship Inference**: Intelligently discovers relationships between your tables.
-   **Seamless Integration**: Once uploaded, the application uses your data as the primary source upon restart.

---

## How It Works

The process is designed to be simple and automated:

1.  **Upload**: You upload an `.xlsx` file through the "Data Upload" tab in the Gradio interface.
2.  **Convert**: The system reads the Excel file and converts each sheet into a separate, optimized Parquet file. These files are saved in the `uploaded_data/` directory.
3.  **Analyze**: It then analyzes the structure of each new table to understand its schema, identifying unique identifiers (primary keys) and potential links to other tables (foreign keys).
4.  **Infer**: Based on the column names (e.g., `customer_ID` in one table and `customer_ID` in another), it automatically infers the relationships required to build the KumoRFM knowledge graph.
5.  **Restart & Reload**: After the conversion is complete, you must **restart the application**. On startup, the application prioritizes the `uploaded_data/` directory, loading your new dataset as the primary data source for all analysis and predictions.

---

## Excel File Requirements

To ensure successful conversion and analysis, your Excel file should follow these guidelines:

-   **File Format**: Must be an Excel file with the `.xlsx` extension.
-   **One Sheet per Table**: Each sheet in your workbook should represent a distinct data table (e.g., `customers`, `claims`, `policies`).
-   **Clear Headers**: The first row of each sheet must contain clear, descriptive column headers.
-   **Consistent Naming for Keys**: For automatic relationship inference to work best, use consistent naming conventions for your ID columns.
    -   **Primary Keys**: Name the primary identifier of a table with a suffix like `_ID` or `_number` (e.g., `customer_ID`, `policy_ID`, `claim_number`).
    -   **Foreign Keys**: When referencing another table, use the exact same column name as that table's primary key (e.g., the `claims` table should have a `customer_ID` column to link to the `customers` table).
-   **Date/Time Columns**: Ensure columns containing dates or timestamps are formatted as date/time types in Excel.
-   **Clean Data**: Avoid merged cells, subtotals, or other non-tabular data within your sheets.

### Example Structure:

**Sheet 1: `customers`**
| customer_ID | name | birth_date |
|---|---|---|
| CUST101 | John Doe | 1985-05-10 |

**Sheet 2: `claims`**
| claim_ID | customer_ID | claim_date | amount |
|---|---|---|---|
| CLM5001 | CUST101 | 2023-11-01 | 1500.00 |

---

## Step-by-Step Usage Guide

1.  **Launch the Application**: Start the FraudAGENT application as usual.

2.  **Navigate to the Upload Tab**: Open the web interface and click on the **📤 Data Upload** tab.

3.  **Upload Your File**: Drag and drop your `.xlsx` file into the upload box, or click to browse and select it.

4.  **Start the Conversion**: Click the **🚀 Convert to Parquet** button. The process will begin, and you will see status updates in real-time.

5.  **Review the Results**: Once complete, the interface will display:
    -   A **status message** confirming the conversion.
    -   A detailed **Schema Information** panel showing the structure of your new tables.
    -   An **Inferred Relationships** panel showing how your tables are linked.

6.  **Restart the Application**: This is a **critical step**. For the application to use your newly uploaded data, you must stop and restart the application (e.g., by stopping the `docker-compose` or Python script and running it again).

7.  **Verify the New Data Source**: After restarting, the "Settings" tab should show that the data source is now the `uploaded_data/` directory. All queries and predictions will now run against your own data.

---

## Technical Details

-   **Output Directory**: All converted Parquet files are stored in the `/home/ubuntu/insurance-claims-kumo-agent/uploaded_data/` directory within the application's environment.
-   **Metadata File**: A summary of the conversion, including schema and relationship info, is saved to `uploaded_data/upload_metadata.json`.
-   **Data Source Priority**: The application loads data in the following order of priority:
    1.  `uploaded_data/` (if it exists and is not empty)
    2.  The path specified in the `INSURANCE_DATA_PATH` environment variable.
    3.  The default `data/` directory.
-   **Overwriting Data**: Uploading a new file will overwrite the contents of the `uploaded_data/` directory.

---

## Troubleshooting

-   **Error during conversion**: This is often due to an issue with the Excel file's format. Ensure it meets all the requirements listed above, especially regarding clear headers and no merged cells.
-   **No relationships inferred**: This happens if the system cannot automatically detect links. Check that your foreign key columns have names that exactly match the primary key columns in other tables (e.g., `customer_ID` and `customer_ID`).
-   **Old data is still being used after upload**: You must restart the application after a successful conversion. The data source is only determined at startup.
-   **Permission errors**: Ensure the application has write permissions to the `uploaded_data/` directory.

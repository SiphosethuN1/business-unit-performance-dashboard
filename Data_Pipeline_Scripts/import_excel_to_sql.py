import pandas as pd
from pathlib import Path
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text


# ============================================================
# CONFIGURATION
# ============================================================

SERVER = r"SIPHOSETHU-NYAW\SQLEXPRESS"
DATABASE = "PortfolioAnalytics"

# Python script location:
# C:\Users\DELL\OneDrive\Documents\GitHub\PythonScript
#
# Excel files location:
# C:\Users\DELL\OneDrive\Documents\GitHub

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent

SUMMARY_FILE = DATA_DIR / "Employee_Activity_Summary.xlsx"
DETAIL_FILE = DATA_DIR / "Employee_Activity_Detail.xlsx"


# ============================================================
# CHECK FILES EXIST
# ============================================================

print("=" * 60)
print("CHECKING SOURCE FILES")
print("=" * 60)

files = [
    SUMMARY_FILE,
    DETAIL_FILE
]

for file in files:
    if not file.exists():
        raise FileNotFoundError(
            f"\nFile not found:\n{file}"
        )

    print(f"Found: {file.name}")

print("\nAll source files found successfully.")


# ============================================================
# SQL SERVER CONNECTION
# ============================================================

print("\n" + "=" * 60)
print("CONNECTING TO SQL SERVER")
print("=" * 60)

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

connection_url = (
    "mssql+pyodbc:///?odbc_connect="
    + quote_plus(connection_string)
)

engine = create_engine(connection_url)


try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("SQL Server connection successful.")
    print(f"Server:   {SERVER}")
    print(f"Database: {DATABASE}")

except Exception as error:
    print("\nSQL Server connection failed.")
    print(error)
    raise


# ============================================================
# IMPORT FUNCTION
# ============================================================

def import_excel_to_sql(file_path, table_name):

    print("\n" + "=" * 60)
    print(f"IMPORTING: {file_path.name}")
    print("=" * 60)

    # --------------------------------------------------------
    # Read Excel
    # --------------------------------------------------------

    try:
        df = pd.read_excel(
            file_path,
            engine="openpyxl"
        )

        print("\nExcel file loaded successfully.")
        print(f"Rows:    {len(df)}")
        print(f"Columns: {len(df.columns)}")

        print("\nColumns detected:")

        for column in df.columns:
            print(f" - {column}")

    except Exception as error:
        print("\nFailed to read Excel file.")
        print(error)
        raise


    # --------------------------------------------------------
    # Remove completely empty rows
    # --------------------------------------------------------

    original_rows = len(df)

    df = df.dropna(how="all")

    removed_rows = original_rows - len(df)

    if removed_rows > 0:
        print(
            f"\nRemoved {removed_rows} completely empty row(s)."
        )


    # --------------------------------------------------------
    # Clean column names
    # --------------------------------------------------------

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]


    # --------------------------------------------------------
    # Import into SQL Server
    # --------------------------------------------------------

    print(f"\nImporting into dbo.{table_name}...")

    try:
        df.to_sql(
            name=table_name,
            con=engine,
            schema="dbo",
            if_exists="replace",
            index=False,
            chunksize=1000
        )

        print(
            f"Successfully imported into dbo.{table_name}"
        )

    except Exception as error:
        print("\nSQL import failed.")
        print(error)
        raise


    # --------------------------------------------------------
    # Verify SQL row count
    # --------------------------------------------------------

    try:
        with engine.connect() as connection:

            result = connection.execute(
                text(
                    f"SELECT COUNT(*) "
                    f"FROM dbo.{table_name}"
                )
            )

            sql_rows = result.scalar()

        print("\nImport verification:")
        print(f"Excel rows: {len(df)}")
        print(f"SQL rows:   {sql_rows}")

        if len(df) == sql_rows:

            print(
                "SUCCESS: Excel and SQL row counts match."
            )

        else:

            print(
                "WARNING: Excel and SQL row counts do not match."
            )

    except Exception as error:
        print("\nVerification failed.")
        print(error)
        raise

    return len(df)


# ============================================================
# IMPORT EMPLOYEE ACTIVITY SUMMARY
# ============================================================

summary_rows = import_excel_to_sql(
    SUMMARY_FILE,
    "employee_activity_summary"
)


# ============================================================
# IMPORT EMPLOYEE ACTIVITY DETAIL
# ============================================================

detail_rows = import_excel_to_sql(
    DETAIL_FILE,
    "employee_activity_detail"
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("ETL PROCESS COMPLETED")
print("=" * 60)

print(
    f"employee_activity_summary : {summary_rows} rows"
)

print(
    f"employee_activity_detail  : {detail_rows} rows"
)

print("\nBoth datasets were imported successfully.")

print(
    "\nSQL tables created:"
)

print(
    "dbo.employee_activity_summary"
)

print(
    "dbo.employee_activity_detail"
)

print("\nReady for Power BI.")
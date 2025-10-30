import pandas as pd
from sqlalchemy import create_engine
import pyodbc

def connect_mysql(server,database,username,password):

    # ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
    conn_str = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={server};"
            f"DATABASE={database};"
            "ENCRYPT=yes;"
            f"UID={username};"
            f"PWD={password};"
        )
    cnxn = pyodbc.connect(conn_str)
    print(f"✅ Connected successfully to database '{database}' on '{server}'")
    return cnxn
    

def execute_sql_file(connection, sql_file_path: str, **params) -> pd.DataFrame:
    """
    Execute a SQL query from a .sql file using a pyodbc connection.

    Args:
        connection: Active pyodbc connection.
        sql_file_path (str): Path to the .sql file.
        params: the year we want to replace in .sql files

    Returns:
        pd.DataFrame: Query result as a DataFrame.
    """
    if connection is None:
        print("❌ No valid database connection provided.")
        return pd.DataFrame()

    try:
        # Read SQL file
        with open(sql_file_path, "r", encoding="utf-8") as f:
            query = f.read().strip()

        # Replace ano in queries with a year
        query = query.format(**params)

        # Run query
        df = pd.read_sql(query, connection)
        print(f"✅ Executed query from '{sql_file_path}' — retrieved {len(df)} rows")
        return df

    except Exception as e:
        print(f"❌ Error executing SQL file '{sql_file_path}': {e}")
        return pd.DataFrame()
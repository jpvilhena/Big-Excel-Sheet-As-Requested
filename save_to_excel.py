import pandas as pd

def save_multiple_dataframes_to_excel(dfs: dict[str, pd.DataFrame], filename: str = "Tabelao.xlsx"):
    """
    Saves multiple DataFrames to a single Excel file.
    Each key in `dfs` will be used as the sheet name.

    Args:
        dfs (dict[str, pd.DataFrame]): Dictionary of {sheet_name: dataframe}.
        filename (str): Output Excel file name.
    """
    try:
        with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
            for sheet_name, df in dfs.items():
                # Ensure valid Excel sheet name (max 31 chars, no invalid chars)
                safe_name = sheet_name[:31].replace("/", "_").replace("\\", "_")
                df.to_excel(writer, index=False, sheet_name=safe_name)
        print(f"✅ All DataFrames saved successfully to '{filename}'")
    except Exception as e:
        print(f"❌ Error saving file: {e}")
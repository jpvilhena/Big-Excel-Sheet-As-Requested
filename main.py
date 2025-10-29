import os
from conectionDW import connect_mysql, get_tables_rows, execute_sql_file
from save_to_excel import save_multiple_dataframes_to_excel
import streamlit as st
import io


# We decide what tables will be in this dict, the keys are the tables and their dataframes will be the values
Tables = {

}


# We decide the sql files that will be read here, same logic as above
SQL_files = {

}

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="BI Data Extractor", layout="wide")
st.title("📊 BI Data Extractor")

with st.sidebar:
    st.header("🔑 Database Connection")
    server = st.text_input("Server", value=os.getenv("Servidor", ""))
    database = st.text_input("Database", value=os.getenv("Banco", ""))
    username = st.text_input("Username", value=os.getenv("Usuario", ""))
    password = st.text_input("Password", value=os.getenv("Senha", ""), type="password")
    year = st.number_input("Min year", min_value=2022, max_value=2025, value=2025)

get_tables = st.button("Get Tables")
run_queries = st.button("Run Queries")
engine = None

# Function to start the engine that connects to the database
def start_engine():
    global engine
    st.write("Connecting to database...")
    try:
        engine = connect_mysql(
            username=username,
            password=password,
            server=server,
            database=database,
        )
        st.success("✅ Connected successfully!")
    except Exception as e:
        st.error(f"❌ Connection failed: {e}")
        st.stop()


if get_tables:
    # Check if engine has been set
    if engine == None:
        start_engine()

    # Containers for progress and results
    progress = st.progress(0)
    dfs = {}

    # Iterate over each key and get the rows from their tables using i for the progress bar
    st.subheader("📋 Fetching tables...")
    for i, t in enumerate(Tables.keys()):
        try:
            Tables[t] = get_tables_rows(engine, t, year=year)
            st.write(f"✅ {t} loaded ({len(Tables[t])} rows)")
        except Exception as e:
            st.warning(f"⚠️ Error loading {t}: {e}")
        progress.progress((i + 1) / len(Tables))

    # Save first Excel file
    st.write("💾 Creating Excel for tables...")
    buf1 = io.BytesIO()
    save_multiple_dataframes_to_excel(Tables, buf1)
    buf1.seek(0)

    st.download_button(
        label="⬇️ Download Tables Excel",
        data=buf1,
        file_name="Tabelas_BI_Vendas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

if run_queries:
    # Check if engine has been set
    if engine == None:
        start_engine(engine)

    # Same logic as above but now with the queries used in the BI
    st.subheader("🧮 Executing SQL files...")
    # Dict to recieve dataframes from sql querries ran below
    dfs = {}
    for i, (name, path) in enumerate(SQL_files.items()):
        try:
            dfs[name] = execute_sql_file(engine, path)
            st.write(f"✅ {name} ({path}) executed successfully")
        except Exception as e:
            st.warning(f"⚠️ Error executing {name}: {e}")
        progress.progress((i + 1) / len(SQL_files))
    
    # Save second Excel file
    st.write("💾 Creating Excel for SQL results...")
    buf2 = io.BytesIO()
    save_multiple_dataframes_to_excel(dfs, buf2)
    buf2.seek(0)

    st.download_button(
        label="⬇️ Download SQL Results Excel",
        data=buf2,
        file_name="Resultados_SQL_BI_Vendas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
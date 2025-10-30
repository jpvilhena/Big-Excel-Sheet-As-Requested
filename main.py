import os
from conectionDW import connect_mysql, execute_sql_file
from save_to_excel import save_multiple_dataframes_to_excel
import streamlit as st
import io


# We take the sql files that will be read here, everything within the folder Integracoes
SQL_files1 = {}
for entry in os.listdir("Integracoes"):
    query_path = (os.path.join("Integracoes",entry))
    SQL_files1.update({entry:query_path})


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

run_queries = st.button("Run Queries")
engine = None

# Function to start the engine that connects to the database
def start_engine():
    global engine
    st.write("Connecting to database...")
    # Getting a connection to the DW by making an engine
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


if run_queries:
    # Check if engine has been set
    if engine == None:
        start_engine()

    # Same logic as above but now with the queries used in the BI
    st.subheader("🧮 Executing SQL files...")
    
    # Dict to recieve dataframes from sql querries run below and Container for progress
    dfs = {}
    progress = st.progress(0)
    
    for i, (name, path) in enumerate(SQL_files1.items()):
        try:
            print(name)
            print(path)
            dfs[name] = execute_sql_file(engine, path, year=2025)
            st.write(f"✅ {name} ({path}) executed successfully")
        except Exception as e:
            st.warning(f"⚠️ Error executing {name}: {e}")
        progress.progress((i + 1) / len(SQL_files1))
    
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
import os
from conectionDW import connect_mysql, get_top_rows, execute_sql_file
from save_to_excel import save_multiple_dataframes_to_excel


# We decide what tables will be in this dict, the keys are the tables and their dataframes will be the values
Tables = {

}


# We decide the sql files that will be read here, same logic as above
SQL_files = {

}


print(f'tcp:{os.getenv("Servidor")}',os.getenv("Banco"),os.getenv("Usuario"),os.getenv("Senha"),)


# Getting a connection to the DW by making an engine
engine = connect_mysql(
    username=os.getenv("Usuario"),
    password=os.getenv("Senha"),
    server=f'tcp:{os.getenv("Servidor")}',
    database=os.getenv("Banco"),
)

# Iterate over each key and get the rows from their tables
for t in Tables:
    Tables[t] = get_top_rows(engine, t, limit=10)

# Dict to recieve dataframes from sql querries run below
dfs = {}

# Same logic as above but now with the queries used in the BI
for name, path in SQL_files.items():
    dfs[path] = execute_sql_file(engine, path)

save_multiple_dataframes_to_excel(Tables, "Tabelao Com todas as tabelas usadas no BI de vendas")
save_multiple_dataframes_to_excel(dfs, "Tabelao com Resultados de SQLs Usados no BI de vendas")
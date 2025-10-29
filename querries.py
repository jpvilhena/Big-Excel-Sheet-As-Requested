import pandas as pd



def get(path,_cnxn):
    try:
        query = open(path / 'vendas.sql', 'r')
        table = pd.read_sql_query(query.read(),_cnxn)
        return table
    except Exception as e:
        print("A conexão com o DW Elos não foi estabelecida.")
        print(e)
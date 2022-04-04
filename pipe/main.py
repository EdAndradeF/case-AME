from get_trat import Tabelas
import pandas as pd
from db_conect import DBConn
from to_sql import DBQuerie


df = pd.read_csv('base_de_respostas_10k_amostra.csv')

connDB = DBConn()
tabelas = Tabelas(df)
lista_df = tabelas.dfs()
BD = DBQuerie(connDB.conn, lista_df)




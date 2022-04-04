import pandas as pd
import psycopg2 as psy
import sqlalchemy as alq


class DBQuerie:

    def __init__(self, conn, obj):

        self.conect = conn
        self.dfs = list(map(self.to_db, obj))

    def to_db(self, df_t):
        df_t[1].to_sql(df_t[0], self.conect, if_exists='replace', index=False)

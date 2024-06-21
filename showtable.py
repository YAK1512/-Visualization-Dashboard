import pandas as pd
from sqlalchemy import create_engine


DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'localhost'
USER = 'postgres'
PASSWORD = 'yash'
PORT = 5432
DATABASE = 'data'

connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"

engine = create_engine(connection_string)
table_name = 'json_data'
df = pd.read_sql_table(table_name, engine)
print(df)

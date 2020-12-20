import sqlite3
import pandas as pd
# connecter à la BDD sqlite3 et transformer une requête en Pandas Dataframe
conn = sqlite3.connect("C:/Users/Epulapp/Desktop/POLYTECH 3A/Projet tutoré/WTF Aspirator/WtfAspirator/src/db.sqlite3")
df = pd.read_sql_query("SELECT * FROM categories", conn)
print(df.head())
conn.close()


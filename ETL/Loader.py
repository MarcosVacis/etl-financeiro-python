import sqlite3

def load_to_sqlite(df, db_path="db/dre.db", table_name="dre"):
    conn = sqlite3.connect(db_path)
    df.to_sql("dre", conn, if_exists="replace", index=False)
    conn.close()

import oracledb

def connect_to_db():
    conn = oracledb.connect(
        user="SYS",
        password="mypassword1",
        dsn="localhost:1521/ORCLCDB",
        mode=oracledb.SYSDBA
    )
    return conn

def get_selected_schema(cursor, tables):
    schema = {}
    for table in tables:
        cursor.execute(f"""
            SELECT column_name, data_type, data_length
            FROM user_tab_columns
            WHERE table_name = '{table.upper()}'
        """)
        columns = cursor.fetchall()
        if columns:
            schema[table.upper()] = [{"column": col, "type": dtype, "length": dlength} 
                for col, dtype, dlength in columns]
        else:
            print(f"⚠️ Table {table} not found or no columns available.")
    return schema
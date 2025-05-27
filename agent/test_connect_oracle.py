import oracledb
import json

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

try:
    conn = oracledb.connect(
        user="SYS",
        password="mypassword1",
        dsn="localhost:1521/ORCLCDB",
        mode=oracledb.SYSDBA
    )
    print("✅ Connected to Oracle!")

    cursor = conn.cursor()
    '''
    cursor.execute("SELECT table_name FROM user_tables")

    print("📦 Tables in your schema:")
    for row in cursor:
        print("-", row[0])
    '''

    target_tables = ['A_COURSES', 'A_DEPARTMENTS', 'A_ENROLLMENTS', 'A_PROFESSORS', 'A_STUDENTS']
    schema = get_selected_schema(cursor, target_tables)
    print(json.dumps(schema, indent=2))

except Exception as e:
    print("❌ Connection failed:", e)

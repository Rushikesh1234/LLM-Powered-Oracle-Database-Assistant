from db import connect_to_db, get_selected_schema
from llm import generate_sql
import json

def run():
    conn = connect_to_db()
    print("✅ Connected to Oracle!")

    cursor = conn.cursor()
    target_tables = ['A_COURSES', 'A_DEPARTMENTS', 'A_ENROLLMENTS', 'A_PROFESSORS', 'A_STUDENTS']
    schema_data = get_selected_schema(cursor, target_tables)
    formatted_schema = json.dumps(schema_data, indent=2)

    print("✅ Schema Loaded")
    print(formatted_schema)

    question = input("🔍 Ask your question (natural language):\n> ")
    sql = generate_sql(formatted_schema, question)

    print("\n🧠 Generated SQL:")
    print(sql)

    # Optional: ask before executing
    run_it = input("\nDo you want to run this query? (y/n): ").lower()
    if run_it == 'y':
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if not results:
                print("⚠️ No rows returned.")
            else:
                print("\n📊 Results:")
                for row in results:
                    print(row)
        except Exception as e:
            print("❌ SQL execution error:", e)

if __name__ == "__main__":
    run()

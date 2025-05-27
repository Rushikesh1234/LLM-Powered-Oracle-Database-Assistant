import streamlit as st
from db import connect_to_db, get_selected_schema
from llm import generate_sql
import json

st.set_page_config(page_title="Oracle LLM Assistant", layout="wide")
st.title("🧠 Oracle Database Assistant (LLM-powered)")

question = st.text_area("Ask your database a question (in natural language)", "")

@st.cache_resource
def load_schema():
    conn = connect_to_db()
    cursor = conn.cursor()
    target_tables = ['A_COURSES', 'A_DEPARTMENTS', 'A_ENROLLMENTS', 'A_PROFESSORS', 'A_STUDENTS']
    schema = get_selected_schema(cursor, target_tables)
    return json.dumps(schema, indent=2), conn, cursor

if st.button("Generate & Execute SQL"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            schema_text, conn, cursor = load_schema()
            try:
                sql = generate_sql(schema_text, question)
                st.code(sql, language='sql')
            except Exception as e:
                st.error(f"LLM failed: {e}")
                st.stop()

            try:
                cursor.execute(sql)
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                st.success("✅ Query executed successfully")
                st.dataframe([dict(zip(columns, row)) for row in rows])
            except Exception as e:
                st.error(f"DB execution failed: {e}")

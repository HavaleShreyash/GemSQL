from dotenv import load_dotenv
load_dotenv()  # Load env vars

import streamlit as st
import os
import sqlite3

import google.generativeai as gemai

# Config API
gemai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini 
def get_gemini_response(question, prompt):
    model = gemai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt, question])
    return response.text

# Retrieve header names from the database
def get_column_names(db):
    conn = sqlite3.connect(database=db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(DATA)")  # Fetch column information from the table
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]  # Extract column names
    conn.close()
    return column_names

# Retrieve Data from database
def read_sql_query(sql, db):
    conn = sqlite3.connect(database=db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Fetch column names from the database
column_names = get_column_names("DATA.db")

# Generate prompt dynamically based on column names
prompt = f"""You are an expert in converting English questions to SQL queries! The SQL database has the name DATA and the following columns: {', '.join(column_names)}

Example 1: How many entries of records are present?
SELECT COUNT(*) FROM DATA;

Example 2: Tell me all the items based on a specific condition.
SELECT * FROM DATA WHERE COLUMNX="specific_value";

Example 3: Retrieve specific information based on certain conditions.
SELECT COLUMNY FROM DATA WHERE <conditions>;

Example 4: Update a specific column for a specific row.
UPDATE DATA SET COLUMNZ="specific_value" WHERE COLUMN1="specific_condition";

only return the sql query with no formatting and other text
"""

# print(prompt)
# Streamlit App

st.set_page_config(page_title="GemSQL")

# Streamlit App
# st.title("Logo")

# Display image from a file
with open("support/logo.png", "rb") as f:
    image_bytes = f.read()

# st.image(image_bytes, width=200)
# st.image(image_bytes, width=200, output_format='PNG',)
st.image(image_bytes, use_column_width=True)

st.header("Problem:")

question = st.text_input("Input: ", key="input")
submit = st.button("SQL Solution")

if submit:
    response = get_gemini_response(question, prompt)  # This line calls the function get_gemini_response to get the Gemini response
    st.subheader("SQL Query:")
    st.write(response)
    print("Gemini Response:", response)  # Debug print to see Gemini response
    data = read_sql_query(response, "DATA.db")  # This line passes the Gemini response to the function read_sql_query
    st.subheader("Output:")
    for row in data:
        print(row)
        st.subheader(row)
#pip install streamlit
import streamlit as st
import sqlite3

st.title("Expense Tracker")
st.divider()
# Connect to SQLite database
conn = sqlite3.connect('expenses.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS expenses
             (date text, amount real, description text, category text)''')

# User input form
date = st.date_input('Date')
amount = st.number_input('Amount')
description = st.text_input('Description')
category = st.selectbox('Category', ['Food', 'Transportation', 'Entertainment', 'Education', 'Travelling', 'Other'])

if st.button('Submit'):
    c.execute("INSERT INTO expenses VALUES (?, ?, ?, ?)", (date, amount, description, category))
    conn.commit()
    st.success('Expense added successfully!')
    
st.divider()

import pandas as pd
import plotly.express as px

# Load data from SQLite
df = pd.read_sql_query("SELECT * FROM expenses", conn)

# Category-wise expenditure
category_expenditure = df.groupby('category')['amount'].sum().reset_index()

# Plotting
fig = px.bar(category_expenditure, x='category', y='amount', title='Category-wise Expenditure')
st.plotly_chart(fig)


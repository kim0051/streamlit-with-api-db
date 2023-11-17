import streamlit as st
import mysql.connector
from st_pages import add_page_title

add_page_title(layout="wide")

# Create a connection to MySQL database
mysql_db = mysql.connector.connect(
    host="localhost",
    user="ryan",
    password="samarinda123",
    database="jwt_api_netcore"
)

# Create a cursor to execute MySQL queries
cursor = mysql_db.cursor()
cursor.execute("SELECT * FROM tb_approval")
result = cursor.fetchall()
for x in result:
    st.write(x)

st.write("This is just a sample page!")
import datetime
import pyodbc
import streamlit as st
from st_pages import add_page_title
import pandas as pd
from _mylibs import *

add_page_title(layout="wide")

st.write("SQL Data")

conn = pyodbc.connect("DRIVER={SQL Server}; Server="+st.secrets.db_credentials.server+"; UID="+st.secrets.db_credentials.username+"; PWD="+st.secrets.db_credentials.password+"; Database="+st.secrets.db_credentials.database1+"")

@st.cache_data(ttl=300)
def filterData(area, equipment, pit, material, series, start_date, end_date):
    # Add your filtering logic here
    query = "SELECT * FROM "+st.secrets.tbl_loaderp+" where date >= '" + start_date.strftime("%Y-%m-%d") + "' and date <= '" + end_date.strftime("%Y-%m-%d") + "'"
    if(area != 'ALL'):
        query += " and area = '" + area + "'"
    if(equipment != 'ALL'):
        query += " and EQUIPMENT = '" + equipment + "'"
    if(pit != 'ALL'):
        query += " and PIT = '" + pit + "'"
    if(material != 'ALL'):
        query += " and MATERIAL = '" + material + "'"
    data = pd.read_sql(query, conn)
    st.dataframe(data, use_container_width=True)
    st.markdown("<center><h5>SUM DATA " + series + " FROM " + start_date.strftime("%Y-%m-%d") + " TO " + end_date.strftime("%Y-%m-%d") + "</h5></center>", unsafe_allow_html=True)
    # Chart by area
    query_chart1 = "SELECT area, SUM(" + series + ") as "+series+" FROM "+st.secrets.tbl_loaderp+" where date >= '" + start_date.strftime("%Y-%m-%d") + "' and date <= '" + end_date.strftime("%Y-%m-%d") + "' GROUP BY area"
    data_chart1 = pd.read_sql(query_chart1, conn)
    chart1 = pd.DataFrame(data_chart1)
    st.write("Bar Chart by Area")
    st.bar_chart(data=chart1, use_container_width=True, x='area', y=series, color="#8ecae6")
    
    # Chart by date
    query_chart2 = "SELECT DATE, SUM(" + series + ") as "+series+" FROM "+st.secrets.tbl_loaderp+" where date >= '" + start_date.strftime("%Y-%m-%d") + "' and date <= '" + end_date.strftime("%Y-%m-%d") + "' GROUP BY DATE"
    data_chart2 = pd.read_sql(query_chart2, conn)
    chart2 = pd.DataFrame(data_chart2)
    st.write("Bar Chart by Loader")
    st.bar_chart(data=chart2, use_container_width=True, x='DATE', y=series, color="#ffe6a7")

    # Chart by equipment
    query_chart3 = "SELECT EQUIPMENT, SUM(" + series + ") as "+series+" FROM "+st.secrets.tbl_loaderp+" where date >= '" + start_date.strftime("%Y-%m-%d") + "' and date <= '" + end_date.strftime("%Y-%m-%d") + "' GROUP BY EQUIPMENT"
    data_chart3 = pd.read_sql(query_chart3, conn)
    chart3 = pd.DataFrame(data_chart3)
    st.write("Bar Chart by Loader")
    st.bar_chart(data=chart3, use_container_width=True, x='EQUIPMENT', y=series, color="#283618")

    # Chart by pit
    query_chart4 = "SELECT PIT, SUM(" + series + ") as "+series+" FROM "+st.secrets.tbl_loaderp+" where date >= '" + start_date.strftime("%Y-%m-%d") + "' and date <= '" + end_date.strftime("%Y-%m-%d") + "' GROUP BY PIT"
    data_chart4 = pd.read_sql(query_chart4, conn)
    chart4 = pd.DataFrame(data_chart4)
    st.write("Bar Chart by Pit")
    st.bar_chart(data=chart4, use_container_width=True, x='PIT', y=series, color="#023047")

    # Chart by material
    query_chart5 = "SELECT MATERIAL, SUM(" + series + ") as "+series+" FROM "+st.secrets.tbl_loaderp+" where date >= '" + start_date.strftime("%Y-%m-%d") + "' and date <= '" + end_date.strftime("%Y-%m-%d") + "' GROUP BY MATERIAL"
    data_chart5 = pd.read_sql(query_chart5, conn)
    chart5 = pd.DataFrame(data_chart5)
    st.write("Bar Chart by Material")
    st.bar_chart(data=chart5, use_container_width=True, x='MATERIAL', y=series, color="#ffb703")
    pass

@st.cache_data(ttl=300)
def runQuery(query):
    data = pd.read_sql(query, conn)
    return data

area = runQuery("SELECT DISTINCT area FROM "+st.secrets.tbl_loaderp+"")
equipment = runQuery("SELECT DISTINCT EQUIPMENT FROM "+st.secrets.tbl_loaderp+"")
pit = runQuery("SELECT DISTINCT PIT FROM "+st.secrets.tbl_loaderp+"")
material = runQuery("SELECT DISTINCT MATERIAL FROM "+st.secrets.tbl_loaderp+"")
new_area = loopFetchData(area['area'])
new_equipment = loopFetchData(equipment['EQUIPMENT'])
new_pit = loopFetchData(pit['PIT'])
new_material = loopFetchData(material['MATERIAL'])
series = ["HOUR", "WH", "DELAY", "IDLE", "DOWN", "TOTAL_TONNAGE", "TOTAL_VOLUME", "DISTANCE", "PRODUCTIVITY_LOADER"]
with st.expander("Filter Data", expanded=True):
    value_area = st.selectbox("Area", new_area)
    value_equipment = st.selectbox("Equipment", new_equipment)
    value_pit = st.selectbox("Pit", new_pit)
    value_material = st.selectbox("Material", new_material)
    value_series = st.selectbox("Series", series)
    
    timeday = datetime.datetime.now()
    temp_prev_month = timeday.month - 1
    first_day = datetime.date(timeday.year, 1, 1)

    today = datetime.date(timeday.year, timeday.month, timeday.day)
    previouse_month = datetime.date(timeday.year, temp_prev_month, timeday.day)
    d = st.date_input(
        "Select date range",
        (previouse_month, today),
        first_day,
        today,
        format="YYYY/MM/DD",
    )

    if(st.button('Filter Data')):
        if((d[1]-d[0]).days > 31):
            st.error("Date range cannot more than 1 month")
        else:
            filterData(value_area, value_equipment, value_pit, value_material, value_series, d[0], d[1])
import datetime
import pyodbc
import streamlit as st
from st_pages import add_page_title
import pandas as pd

add_page_title(layout="wide")

st.write("SQL Data")

conn = pyodbc.connect("DRIVER={SQL Server}; Server=kpcsgt-db04; UID=test_ryan; PWD=samarinda123; Database=TEST_DEV")

def filterData(area, equipment, pit, material, series, start_date, end_date):
    # Add your filtering logic here
    query = "SELECT * FROM loader_performances where date >= '" + start_date.strftime("%Y-%m-%d") + "' and date <= '" + end_date.strftime("%Y-%m-%d") + "'"
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
    query_chart1 = "SELECT area, SUM(" + series + ") as "+series+" FROM loader_performances where date >= '" + start_date.strftime("%Y-%m-%d") + "' and date <= '" + end_date.strftime("%Y-%m-%d") + "' GROUP BY area"
    data_chart1 = pd.read_sql(query_chart1, conn)
    chart1 = pd.DataFrame(data_chart1)
    st.write("Bar Chart by Area")
    st.bar_chart(data=chart1, use_container_width=True, x='area', y=series, color="#8ecae6")
    
    # Chart by date
    query_chart2 = "SELECT DATE, SUM(" + series + ") as "+series+" FROM loader_performances where date >= '" + start_date.strftime("%Y-%m-%d") + "' and date <= '" + end_date.strftime("%Y-%m-%d") + "' GROUP BY DATE"
    data_chart2 = pd.read_sql(query_chart2, conn)
    chart2 = pd.DataFrame(data_chart2)
    st.write("Bar Chart by Loader")
    st.bar_chart(data=chart2, use_container_width=True, x='DATE', y=series, color="#ffe6a7")

    # Chart by equipment
    query_chart3 = "SELECT EQUIPMENT, SUM(" + series + ") as "+series+" FROM loader_performances where date >= '" + start_date.strftime("%Y-%m-%d") + "' and date <= '" + end_date.strftime("%Y-%m-%d") + "' GROUP BY EQUIPMENT"
    data_chart3 = pd.read_sql(query_chart3, conn)
    chart3 = pd.DataFrame(data_chart3)
    st.write("Bar Chart by Loader")
    st.bar_chart(data=chart3, use_container_width=True, x='EQUIPMENT', y=series, color="#283618")

    # Chart by pit
    query_chart4 = "SELECT PIT, SUM(" + series + ") as "+series+" FROM loader_performances where date >= '" + start_date.strftime("%Y-%m-%d") + "' and date <= '" + end_date.strftime("%Y-%m-%d") + "' GROUP BY PIT"
    data_chart4 = pd.read_sql(query_chart4, conn)
    chart4 = pd.DataFrame(data_chart4)
    st.write("Bar Chart by Pit")
    st.bar_chart(data=chart4, use_container_width=True, x='PIT', y=series, color="#023047")

    # Chart by material
    query_chart5 = "SELECT MATERIAL, SUM(" + series + ") as "+series+" FROM loader_performances where date >= '" + start_date.strftime("%Y-%m-%d") + "' and date <= '" + end_date.strftime("%Y-%m-%d") + "' GROUP BY MATERIAL"
    data_chart5 = pd.read_sql(query_chart5, conn)
    chart5 = pd.DataFrame(data_chart5)
    st.write("Bar Chart by Material")
    st.bar_chart(data=chart5, use_container_width=True, x='MATERIAL', y=series, color="#ffb703")
    
    pass

area = pd.read_sql("SELECT DISTINCT area FROM loader_performances", conn)
equipment = pd.read_sql("SELECT DISTINCT EQUIPMENT FROM loader_performances", conn)
pit = pd.read_sql("SELECT DISTINCT PIT FROM loader_performances", conn)
material = pd.read_sql("SELECT DISTINCT MATERIAL FROM loader_performances", conn)
all = pd.Series(['ALL'])
new_area = all.append(area['area'], ignore_index=True)
new_equipment = all.append(equipment['EQUIPMENT'], ignore_index=True)
new_pit = all.append(pit['PIT'], ignore_index=True)
new_material = all.append(material['MATERIAL'], ignore_index=True)
series = pd.Series(["HOUR", "WH", "DELAY", "IDLE", "DOWN", "TOTAL_TONNAGE", "TOTAL_VOLUME", "DISTANCE", "PRODUCTIVITY_LOADER"])
with st.expander("Filter Data", expanded=True):
    value_area = st.selectbox("Area", new_area)
    value_equipment = st.selectbox("Equipment", new_equipment)
    value_pit = st.selectbox("Pit", new_pit)
    value_material = st.selectbox("Material", new_material)
    value_series = st.selectbox("Series", series)
    
    timeday = datetime.datetime.now()
    temp_prev_month = timeday.month - 1
    # next_year = today.year + 1
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

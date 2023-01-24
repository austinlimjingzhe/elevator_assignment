# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 08:18:58 2023

@author: Asus
"""
# libraries
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import json
from datetime import datetime
import plotly.express as px

#settings
page_title='Elevator Assignments'
layout='centered'

# load the current dataset
lift_df=pd.read_csv("./lift_assignments.csv")
with open("./companies.json") as f: companies=json.load(f)
timestamp=datetime.today()

# streamlit page
st.set_page_config(page_title=page_title,layout=layout)
st.title(page_title)

# navigation menu
selected=option_menu(
    menu_title=None,
    options=["Data Entry","Data Visualisation"],
    icons=["pencil-fill","bar-chart-fill"],
    orientation="horizontal"
    )

if selected=="Data Entry":
    st.header("Data Entry")
    company = st.selectbox("Which Company Are You From?",companies.keys())
    with st.form("entry_form",clear_on_submit=True):
        col1,col2 = st.columns(2)
        with col1:
            floor=st.radio("Which Floor Are You Going To?",companies[company])
        with col2:
            elevator=st.radio("Which Elevator Were You Assigned?",[f"L{x}" for x in range(1,9)])
        
        submit=st.form_submit_button("Save")
        if submit:
            row=pd.DataFrame([[timestamp,company,floor,elevator]],
                             columns=['timestamp','company','floor','elevator'])
            lift_df=pd.concat([lift_df,row],axis=0)
            lift_df.to_csv("lift_assignments.csv",index=False)
            st.success("Data Saved!")

if selected=='Data Visualisation':
    st.header("Data Visualisation")
    
    if len(lift_df) == 0:
        st.write("There is no data collected yet. Go to the Data Entry tab to collect some data.")
    else:
        lift_vis_df = lift_df.copy()
        lift_vis_df["timestamp"]=pd.to_datetime(lift_vis_df["timestamp"],infer_datetime_format=True)
        lift_vis_df["hour"]=lift_vis_df["timestamp"].dt.hour
        lift_vis_df["day_of_week"]=lift_vis_df["timestamp"].dt.weekday
        
        lift_summary = lift_vis_df.groupby(["day_of_week","hour","company","floor","elevator"]).size().reset_index(name='counts')       
        measures={"Time of Day":"hour","Day of Week":"day_of_week","Destination Floor":"floor","Company":"company"}
        for key,value in measures.items():
            with st.expander(key):
                fig = px.bar(lift_summary, x=value, y="counts", color="elevator")
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
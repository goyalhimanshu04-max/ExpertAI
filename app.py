import streamlit as st
from main_logic import SchedulingLogic
import plotly.express as px

st.set_page_config(page_title="Airline & Cargo Expert System", layout="wide")
st.title("✈️ Expert System for Airline & Cargo Scheduling")

logic = SchedulingLogic()

# Sidebar selection with unique key
system_choice = st.sidebar.selectbox(
    'Choose System:',
    ('Airline Scheduling', 'Cargo Scheduling'),
    key='system_choice'
)

st.sidebar.markdown("---")

if system_choice == 'Airline Scheduling':
    st.subheader("🛫 Airline Scheduling")
    time = st.sidebar.number_input("Enter Flight Time (hrs):", min_value=0, key='flight_time')
    capacity = st.sidebar.number_input("Enter Flight Capacity:", min_value=0, key='flight_capacity')
    ftype = st.sidebar.selectbox("Select Flight Type:", ['Domestic', 'International'], key='flight_type')
    
    if st.sidebar.button("Schedule Flight", key='schedule_flight_btn'):
        result = logic.create_airline_schedule(time, capacity, ftype)
        st.success("Flight scheduled successfully!")
        st.write(result)

    df = logic.get_airline_schedule_summary()
    if not df.empty:
        st.subheader("📊 Flight Schedule Summary")
        st.dataframe(df)

        fig = px.bar(df, x="flight_type", color="flight_status",
                     title="Flights by Type and Status")
        st.plotly_chart(fig, use_container_width=True)

elif system_choice == 'Cargo Scheduling':
    st.subheader("📦 Cargo Scheduling")
    weight = st.sidebar.number_input("Enter Cargo Weight (kg):", min_value=0, key='cargo_weight')
    ctype = st.sidebar.selectbox("Select Cargo Type:", ['Perishable', 'Non-Perishable'], key='cargo_type')
    priority = st.sidebar.selectbox("Select Priority:", ['High', 'Medium', 'Low'], key='cargo_priority')

    if st.sidebar.button("Schedule Cargo", key='schedule_cargo_btn'):
        result = logic.create_cargo_schedule(weight, ctype, priority)
        st.success("Cargo scheduled successfully!")
        st.write(result)

    df = logic.get_cargo_schedule_summary()
    if not df.empty:
        st.subheader("📊 Cargo Schedule Summary")
        st.dataframe(df)

        fig = px.pie(df, names='priority', title='Cargo Priority Distribution')
        st.plotly_chart(fig, use_container_width=True)

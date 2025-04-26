"""
Process Scheduler Simulator with Visualizations

A web-based application that simulates various CPU Scheduling algorithms:
- First Come First Serve (FCFS)
- Shortest Job First (SJF)
- Round Robin (RR)
- Priority Scheduling (both preemptive and non-preemptive)

The application allows users to input process data, choose a scheduling algorithm,
and visualize the results through a Gantt chart and summary tables.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scheduling_algorithms import fcfs, sjf, round_robin, priority_scheduling
from visualization import create_gantt_chart, display_metrics_table, display_schedule_timeline

# Set page configuration
st.set_page_config(
    page_title="Process Scheduler Simulator",
    page_icon="🖥️",
    layout="wide"
)

# Initialize session state for process data
if 'processes' not in st.session_state:
    st.session_state.processes = pd.DataFrame(columns=['pid', 'arrival_time', 'burst_time', 'priority'])

# Function to add a new process
def add_process():
    new_process = {
        'pid': f"P{len(st.session_state.processes) + 1}",
        'arrival_time': arrival_time,
        'burst_time': burst_time,
        'priority': priority
    }
    st.session_state.processes = pd.concat([
        st.session_state.processes,
        pd.DataFrame([new_process])
    ], ignore_index=True)

# Function to remove a process
def remove_process(index):
    st.session_state.processes = st.session_state.processes.drop(index).reset_index(drop=True)
    # Update PIDs to maintain sequential order
    st.session_state.processes['pid'] = [f"P{i+1}" for i in range(len(st.session_state.processes))]

# Function to clear all processes
def clear_processes():
    st.session_state.processes = pd.DataFrame(columns=['pid', 'arrival_time', 'burst_time', 'priority'])

# Function to run the selected scheduling algorithm
def run_scheduler():
    processes = st.session_state.processes.copy()

    if len(processes) == 0:
        st.error("Please add at least one process.")
        return None, None

    if algorithm == "First Come First Serve (FCFS)":
        schedule, metrics = fcfs(processes)
    elif algorithm == "Shortest Job First (SJF)":
        schedule, metrics = sjf(processes)
    elif algorithm == "Round Robin (RR)":
        schedule, metrics = round_robin(processes, time_quantum)
    elif algorithm == "Priority Scheduling":
        schedule, metrics = priority_scheduling(processes, preemptive)

    return schedule, metrics

# App title and description
st.title("Process Scheduler Simulator")
st.markdown("""
This application simulates various CPU scheduling algorithms and visualizes the results.
Add processes with their arrival time, burst time, and priority, then select an algorithm to see how the processes are scheduled.
""")

# Sidebar for algorithm selection and parameters
st.sidebar.header("Scheduling Algorithm")
algorithm = st.sidebar.selectbox(
    "Select Algorithm",
    [
        "First Come First Serve (FCFS)",
        "Shortest Job First (SJF)",
        "Round Robin (RR)",
        "Priority Scheduling"
    ]
)

# Algorithm-specific parameters
if algorithm == "Round Robin (RR)":
    time_quantum = st.sidebar.number_input("Time Quantum", min_value=1, value=2, step=1)
elif algorithm == "Priority Scheduling":
    preemptive = st.sidebar.checkbox("Preemptive", value=False)
else:
    time_quantum = 1
    preemptive = False

# Process input form
st.sidebar.header("Add New Process")
arrival_time = st.sidebar.number_input("Arrival Time", min_value=0, value=0, step=1)
burst_time = st.sidebar.number_input("Burst Time", min_value=1, value=1, step=1)

# Only show priority input for Priority Scheduling
if algorithm == "Priority Scheduling":
    priority = st.sidebar.number_input("Priority (lower value = higher priority)", min_value=1, value=1, step=1)
else:
    # Default priority value for other algorithms
    priority = 1

# Add process button
if st.sidebar.button("Add Process"):
    add_process()

# Clear all processes button
if st.sidebar.button("Clear All Processes"):
    clear_processes()

# Display current processes
st.header("Process Data")
if len(st.session_state.processes) > 0:
    # Create a copy of the DataFrame for display
    display_df = st.session_state.processes.copy()

    # Add column headers based on algorithm
    if algorithm == "Priority Scheduling":
        # Show headers with priority for Priority Scheduling
        st.columns([1, 1, 1, 1, 1], gap="small")[0].write("**Process ID**")
        st.columns([1, 1, 1, 1, 1], gap="small")[1].write("**Arrival Time**")
        st.columns([1, 1, 1, 1, 1], gap="small")[2].write("**Burst Time**")
        st.columns([1, 1, 1, 1, 1], gap="small")[3].write("**Priority**")
        st.columns([1, 1, 1, 1, 1], gap="small")[4].write("**Action**")
    else:
        # Hide priority header for other algorithms
        st.columns([1, 1, 1, 1], gap="small")[0].write("**Process ID**")
        st.columns([1, 1, 1, 1], gap="small")[1].write("**Arrival Time**")
        st.columns([1, 1, 1, 1], gap="small")[2].write("**Burst Time**")
        st.columns([1, 1, 1, 1], gap="small")[3].write("**Action**")

    # Rename columns for display
    display_df = display_df.rename(columns={
        'pid': 'Process ID',
        'arrival_time': 'Arrival Time',
        'burst_time': 'Burst Time',
        'priority': 'Priority'
    })

    # Display the processes with a delete button for each
    if algorithm == "Priority Scheduling":
        # Show priority column for Priority Scheduling
        for i, row in display_df.iterrows():
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
            with col1:
                st.write(row['Process ID'])
            with col2:
                st.write(row['Arrival Time'])
            with col3:
                st.write(row['Burst Time'])
            with col4:
                st.write(row['Priority'])
            with col5:
                if st.button("Remove", key=f"remove_{i}"):
                    remove_process(i)
                    st.experimental_rerun()
    else:
        # Hide priority column for other algorithms
        for i, row in display_df.iterrows():
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            with col1:
                st.write(row['Process ID'])
            with col2:
                st.write(row['Arrival Time'])
            with col3:
                st.write(row['Burst Time'])
            with col4:
                if st.button("Remove", key=f"remove_{i}"):
                    remove_process(i)
                    st.experimental_rerun()
else:
    st.info("No processes added yet. Use the form in the sidebar to add processes.")

# Run simulation button
if st.button("Run Simulation"):
    schedule, metrics = run_scheduler()

    if schedule is not None and metrics is not None:
        st.header("Simulation Results")

        # Display Gantt chart
        st.subheader("Gantt Chart")
        gantt_chart = create_gantt_chart(schedule)
        st.pyplot(gantt_chart)

        # Display process metrics
        st.subheader("Process Metrics")
        display_metrics_table(metrics)

        # Display schedule timeline
        st.subheader("Execution Timeline")
        display_schedule_timeline(schedule)

# Add information about the algorithms
with st.expander("About the Scheduling Algorithms"):
    st.markdown("""
    ### First Come First Serve (FCFS)
    - Processes are executed in the order they arrive
    - Non-preemptive algorithm
    - Simple but can lead to the convoy effect

    ### Shortest Job First (SJF)
    - Executes the process with the shortest burst time first
    - Non-preemptive algorithm
    - Optimal for minimizing average waiting time

    ### Round Robin (RR)
    - Each process gets a fixed time slice (time quantum)
    - Preemptive algorithm
    - Good for time-sharing systems

    ### Priority Scheduling
    - Processes are executed based on priority
    - Can be preemptive or non-preemptive
    - May lead to starvation of low-priority processes
    """)

# Footer
st.markdown("---")
st.markdown("Process Scheduler Simulator - A CPU Scheduling Visualization Tool")

# Run the Streamlit app
if __name__ == "__main__":
    pass  # Streamlit automatically runs the script

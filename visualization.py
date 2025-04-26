"""
Visualization functions for the Process Scheduler Simulator.

This module contains functions to create visualizations for the scheduling results:
- Gantt chart for process execution timeline
- Results table for process metrics
"""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np


def create_gantt_chart(schedule, figsize=(10, 5)):
    """
    Create a Gantt chart visualization for the process execution schedule.

    Args:
        schedule (list): List of dictionaries with process execution details
        figsize (tuple): Figure size (width, height)

    Returns:
        matplotlib.figure.Figure: The Gantt chart figure
    """
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=figsize)

    # Define colors for processes (excluding 'Idle')
    process_ids = sorted(list(set([s['pid'] for s in schedule if s['pid'] != 'Idle'])))
    colors = plt.cm.tab10(np.linspace(0, 1, len(process_ids)))
    color_map = {pid: colors[i] for i, pid in enumerate(process_ids)}
    color_map['Idle'] = 'lightgray'  # Idle time is gray

    # Plot each process execution
    y_pos = 0
    for i, proc in enumerate(schedule):
        pid = proc['pid']
        start_time = proc['start_time']
        end_time = proc['end_time']
        duration = end_time - start_time

        # Plot the process bar
        ax.barh(y_pos, duration, left=start_time, height=0.5,
                color=color_map[pid], alpha=0.8,
                edgecolor='black', linewidth=1)

        # Add process label in the middle of the bar
        if duration > 0.5:  # Only add text if the bar is wide enough
            # Add process ID in the middle
            ax.text(start_time + duration/2, y_pos, pid,
                    ha='center', va='center', color='black', fontweight='bold')

    # Set labels and title
    ax.set_xlabel('Time')
    ax.set_yticks([])  # Hide y-axis ticks
    ax.set_title('Process Execution Gantt Chart')

    # Set custom x-axis ticks at process start and end times
    all_times = []
    for proc in schedule:
        all_times.append(proc['start_time'])
        all_times.append(proc['end_time'])

    # Remove duplicates and sort
    all_times = sorted(list(set(all_times)))

    # Set the custom ticks
    ax.set_xticks(all_times)
    ax.set_xticklabels(all_times)

    # Add grid lines
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    # Add legend
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color_map[pid]) for pid in color_map]
    ax.legend(legend_handles, color_map.keys(), loc='upper right', title='Process ID')

    # Adjust layout
    plt.tight_layout()

    return fig


def display_metrics_table(metrics):
    """
    Display a table with process metrics.

    Args:
        metrics (pd.DataFrame): DataFrame with process metrics
    """
    # Format the metrics table for display
    display_df = metrics.copy()

    # Rename columns for better readability
    display_df = display_df.rename(columns={
        'pid': 'Process ID',
        'arrival_time': 'Arrival Time',
        'burst_time': 'Burst Time',
        'priority': 'Priority',
        'completion_time': 'Completion Time',
        'turnaround_time': 'Turnaround Time',
        'waiting_time': 'Waiting Time'
    })

    # Display the table
    st.dataframe(display_df, use_container_width=True)

    # Calculate and display average metrics
    avg_turnaround = metrics['turnaround_time'].mean()
    avg_waiting = metrics['waiting_time'].mean()

    st.write(f"**Average Turnaround Time:** {avg_turnaround:.2f}")
    st.write(f"**Average Waiting Time:** {avg_waiting:.2f}")


def display_schedule_timeline(schedule):
    """
    Display a timeline of the process execution schedule.

    Args:
        schedule (list): List of dictionaries with process execution details
    """
    # Display the timeline
    st.write("**Process Execution Timeline:**")

    # Group processes by ID to show a summary
    process_timelines = {}

    for proc in schedule:
        pid = proc['pid']
        start_time = proc['start_time']
        end_time = proc['end_time']

        if pid not in process_timelines:
            process_timelines[pid] = []

        process_timelines[pid].append((start_time, end_time))

    # Display detailed timeline
    st.write("**Detailed Timeline:**")
    for i, proc in enumerate(schedule):
        pid = proc['pid']
        start_time = proc['start_time']
        end_time = proc['end_time']
        duration = end_time - start_time

        if pid == 'Idle':
            st.write(f"Time {start_time} - {end_time}: CPU Idle ({duration} time units)")
        else:
            st.write(f"Time {start_time} - {end_time}: Process {pid} executing ({duration} time units)")

    # Display process-wise summary in the requested format
    st.write("**Process Execution Timeline (Concise Format):**")

    # Create a concise timeline string
    timeline_parts = []
    for pid, times in process_timelines.items():
        if pid != 'Idle':
            for start, end in times:
                timeline_parts.append(f"{pid}:{start}-{end}")

    # Sort by start time
    timeline_parts.sort(key=lambda x: int(x.split(':')[1].split('-')[0]))

    # Join all parts with commas
    concise_timeline = ','.join(timeline_parts)

    # Display the concise timeline
    st.code(concise_timeline)

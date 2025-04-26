"""
Process Scheduling Algorithms Implementation

This module contains implementations of various CPU scheduling algorithms:
- First Come First Serve (FCFS)
- Shortest Job First (SJF)
- Round Robin (RR)
- Priority Scheduling (both preemptive and non-preemptive)
"""

import pandas as pd
import numpy as np


def fcfs(processes):
    """
    First Come First Serve (FCFS) scheduling algorithm.
    
    Args:
        processes (pd.DataFrame): DataFrame with columns 'pid', 'arrival_time', 'burst_time'
        
    Returns:
        tuple: (schedule, metrics)
            - schedule: List of dictionaries with process execution details
            - metrics: DataFrame with process metrics
    """
    # Sort processes by arrival time
    processes = processes.sort_values(by=['arrival_time', 'pid']).reset_index(drop=True)
    
    n = len(processes)
    current_time = 0
    completion_time = [0] * n
    turnaround_time = [0] * n
    waiting_time = [0] * n
    
    # Schedule to store the execution sequence for Gantt chart
    schedule = []
    
    for i in range(n):
        # If there's a gap between processes
        if current_time < processes.loc[i, 'arrival_time']:
            # Add idle time to schedule
            if current_time < processes.loc[i, 'arrival_time']:
                schedule.append({
                    'pid': 'Idle',
                    'start_time': current_time,
                    'end_time': processes.loc[i, 'arrival_time']
                })
            current_time = processes.loc[i, 'arrival_time']
        
        # Add process to schedule
        schedule.append({
            'pid': processes.loc[i, 'pid'],
            'start_time': current_time,
            'end_time': current_time + processes.loc[i, 'burst_time']
        })
        
        # Update times
        completion_time[i] = current_time + processes.loc[i, 'burst_time']
        turnaround_time[i] = completion_time[i] - processes.loc[i, 'arrival_time']
        waiting_time[i] = turnaround_time[i] - processes.loc[i, 'burst_time']
        
        # Update current time
        current_time = completion_time[i]
    
    # Create metrics DataFrame
    metrics = processes.copy()
    metrics['completion_time'] = completion_time
    metrics['turnaround_time'] = turnaround_time
    metrics['waiting_time'] = waiting_time
    
    return schedule, metrics


def sjf(processes):
    """
    Shortest Job First (SJF) scheduling algorithm (non-preemptive).
    
    Args:
        processes (pd.DataFrame): DataFrame with columns 'pid', 'arrival_time', 'burst_time'
        
    Returns:
        tuple: (schedule, metrics)
            - schedule: List of dictionaries with process execution details
            - metrics: DataFrame with process metrics
    """
    # Create a copy to avoid modifying the original DataFrame
    df = processes.copy()
    n = len(df)
    
    # Initialize variables
    current_time = 0
    completed = 0
    completion_time = [0] * n
    turnaround_time = [0] * n
    waiting_time = [0] * n
    is_completed = [False] * n
    
    # Schedule to store the execution sequence for Gantt chart
    schedule = []
    
    while completed != n:
        # Find process with minimum burst time among the arrived processes
        min_burst = float('inf')
        min_index = -1
        
        for i in range(n):
            if df.loc[i, 'arrival_time'] <= current_time and not is_completed[i]:
                if df.loc[i, 'burst_time'] < min_burst:
                    min_burst = df.loc[i, 'burst_time']
                    min_index = i
        
        # If no process is available, add idle time
        if min_index == -1:
            # Find the next process to arrive
            next_arrival = float('inf')
            for i in range(n):
                if not is_completed[i] and df.loc[i, 'arrival_time'] < next_arrival:
                    next_arrival = df.loc[i, 'arrival_time']
            
            # Add idle time to schedule
            schedule.append({
                'pid': 'Idle',
                'start_time': current_time,
                'end_time': next_arrival
            })
            
            current_time = next_arrival
        else:
            # Add process to schedule
            schedule.append({
                'pid': df.loc[min_index, 'pid'],
                'start_time': current_time,
                'end_time': current_time + df.loc[min_index, 'burst_time']
            })
            
            # Update times
            completion_time[min_index] = current_time + df.loc[min_index, 'burst_time']
            turnaround_time[min_index] = completion_time[min_index] - df.loc[min_index, 'arrival_time']
            waiting_time[min_index] = turnaround_time[min_index] - df.loc[min_index, 'burst_time']
            
            # Update current time and mark process as completed
            current_time = completion_time[min_index]
            is_completed[min_index] = True
            completed += 1
    
    # Create metrics DataFrame
    metrics = df.copy()
    metrics['completion_time'] = completion_time
    metrics['turnaround_time'] = turnaround_time
    metrics['waiting_time'] = waiting_time
    
    return schedule, metrics


def round_robin(processes, time_quantum):
    """
    Round Robin (RR) scheduling algorithm.
    
    Args:
        processes (pd.DataFrame): DataFrame with columns 'pid', 'arrival_time', 'burst_time'
        time_quantum (int): Time quantum for Round Robin
        
    Returns:
        tuple: (schedule, metrics)
            - schedule: List of dictionaries with process execution details
            - metrics: DataFrame with process metrics
    """
    # Create a copy to avoid modifying the original DataFrame
    df = processes.copy()
    n = len(df)
    
    # Initialize variables
    current_time = 0
    completion_time = [0] * n
    remaining_burst_time = df['burst_time'].tolist()
    
    # Schedule to store the execution sequence for Gantt chart
    schedule = []
    
    # Create a ready queue
    ready_queue = []
    
    # Add processes that have arrived at time 0
    for i in range(n):
        if df.loc[i, 'arrival_time'] <= current_time:
            ready_queue.append(i)
    
    # Process until all processes are completed
    while True:
        if not ready_queue:
            # If ready queue is empty but there are still processes to be executed
            if sum(remaining_burst_time) > 0:
                # Find the next process to arrive
                next_arrival = float('inf')
                for i in range(n):
                    if remaining_burst_time[i] > 0 and df.loc[i, 'arrival_time'] < next_arrival:
                        next_arrival = df.loc[i, 'arrival_time']
                
                # Add idle time to schedule
                schedule.append({
                    'pid': 'Idle',
                    'start_time': current_time,
                    'end_time': next_arrival
                })
                
                current_time = next_arrival
                
                # Add processes that have arrived
                for i in range(n):
                    if df.loc[i, 'arrival_time'] <= current_time and remaining_burst_time[i] > 0 and i not in ready_queue:
                        ready_queue.append(i)
            else:
                # All processes are completed
                break
        else:
            # Get the next process from the ready queue
            i = ready_queue.pop(0)
            
            # Calculate execution time for this round
            execution_time = min(time_quantum, remaining_burst_time[i])
            
            # Add process to schedule
            schedule.append({
                'pid': df.loc[i, 'pid'],
                'start_time': current_time,
                'end_time': current_time + execution_time
            })
            
            # Update current time
            current_time += execution_time
            
            # Update remaining burst time
            remaining_burst_time[i] -= execution_time
            
            # Add processes that have arrived during this execution
            for j in range(n):
                if df.loc[j, 'arrival_time'] <= current_time and remaining_burst_time[j] > 0 and j not in ready_queue and j != i:
                    ready_queue.append(j)
            
            # If the process is not completed, add it back to the ready queue
            if remaining_burst_time[i] > 0:
                ready_queue.append(i)
            else:
                # Process is completed, update completion time
                completion_time[i] = current_time
    
    # Calculate turnaround time and waiting time
    turnaround_time = [completion_time[i] - df.loc[i, 'arrival_time'] for i in range(n)]
    waiting_time = [turnaround_time[i] - df.loc[i, 'burst_time'] for i in range(n)]
    
    # Create metrics DataFrame
    metrics = df.copy()
    metrics['completion_time'] = completion_time
    metrics['turnaround_time'] = turnaround_time
    metrics['waiting_time'] = waiting_time
    
    return schedule, metrics


def priority_scheduling(processes, preemptive=False):
    """
    Priority Scheduling algorithm.
    
    Args:
        processes (pd.DataFrame): DataFrame with columns 'pid', 'arrival_time', 'burst_time', 'priority'
        preemptive (bool): Whether to use preemptive priority scheduling
        
    Returns:
        tuple: (schedule, metrics)
            - schedule: List of dictionaries with process execution details
            - metrics: DataFrame with process metrics
    """
    # Create a copy to avoid modifying the original DataFrame
    df = processes.copy()
    n = len(df)
    
    # Initialize variables
    current_time = 0
    completion_time = [0] * n
    remaining_burst_time = df['burst_time'].tolist()
    is_completed = [False] * n
    
    # Schedule to store the execution sequence for Gantt chart
    schedule = []
    
    # Process until all processes are completed
    completed = 0
    prev_process = -1
    
    while completed != n:
        # Find process with highest priority (lowest priority number) among the arrived processes
        highest_priority = float('inf')
        selected_process = -1
        
        for i in range(n):
            if df.loc[i, 'arrival_time'] <= current_time and not is_completed[i]:
                if df.loc[i, 'priority'] < highest_priority:
                    highest_priority = df.loc[i, 'priority']
                    selected_process = i
        
        # If no process is available, add idle time
        if selected_process == -1:
            # Find the next process to arrive
            next_arrival = float('inf')
            for i in range(n):
                if not is_completed[i] and df.loc[i, 'arrival_time'] < next_arrival:
                    next_arrival = df.loc[i, 'arrival_time']
            
            # Add idle time to schedule
            schedule.append({
                'pid': 'Idle',
                'start_time': current_time,
                'end_time': next_arrival
            })
            
            current_time = next_arrival
        else:
            # For non-preemptive, execute the entire process
            if not preemptive:
                # Add process to schedule
                schedule.append({
                    'pid': df.loc[selected_process, 'pid'],
                    'start_time': current_time,
                    'end_time': current_time + remaining_burst_time[selected_process]
                })
                
                # Update times
                current_time += remaining_burst_time[selected_process]
                completion_time[selected_process] = current_time
                remaining_burst_time[selected_process] = 0
                is_completed[selected_process] = True
                completed += 1
            else:
                # For preemptive, execute until a higher priority process arrives
                next_arrival = float('inf')
                for i in range(n):
                    if not is_completed[i] and i != selected_process and df.loc[i, 'arrival_time'] > current_time:
                        next_arrival = min(next_arrival, df.loc[i, 'arrival_time'])
                
                execution_time = min(remaining_burst_time[selected_process], 
                                    next_arrival - current_time if next_arrival != float('inf') else remaining_burst_time[selected_process])
                
                # Add process to schedule if it's different from the previous one or if it's the first process
                if prev_process != selected_process:
                    schedule.append({
                        'pid': df.loc[selected_process, 'pid'],
                        'start_time': current_time,
                        'end_time': current_time + execution_time
                    })
                else:
                    # Extend the previous process's end time
                    schedule[-1]['end_time'] = current_time + execution_time
                
                # Update times
                current_time += execution_time
                remaining_burst_time[selected_process] -= execution_time
                
                # Check if process is completed
                if remaining_burst_time[selected_process] == 0:
                    completion_time[selected_process] = current_time
                    is_completed[selected_process] = True
                    completed += 1
                
                prev_process = selected_process
    
    # Calculate turnaround time and waiting time
    turnaround_time = [completion_time[i] - df.loc[i, 'arrival_time'] for i in range(n)]
    waiting_time = [turnaround_time[i] - df.loc[i, 'burst_time'] for i in range(n)]
    
    # Create metrics DataFrame
    metrics = df.copy()
    metrics['completion_time'] = completion_time
    metrics['turnaround_time'] = turnaround_time
    metrics['waiting_time'] = waiting_time
    
    return schedule, metrics

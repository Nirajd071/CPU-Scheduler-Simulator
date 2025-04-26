# 🖥️ CPU Process Scheduler Simulator

![CPU Scheduler Simulator](https://img.shields.io/badge/CPU-Scheduler_Simulator-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Built_with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.6+-yellow?style=for-the-badge&logo=python)

<div align="center">
  <img src="https://user-images.githubusercontent.com/74038190/212750147-854a394f-fee9-4080-9770-78a4b7ece53f.gif" width="400">
</div>

## ✨ Overview

An interactive web application that simulates various CPU Scheduling algorithms with real-time visualizations. This tool helps students and professionals understand how different scheduling algorithms work by providing visual representations of process execution.

### 🎯 Features

- **Interactive Interface** with auto-selecting input fields
- **Multiple Scheduling Algorithms** (FCFS, SJF, Round Robin, Priority)
- **Rich Visualizations** including Gantt charts and metrics tables
- **Context-aware inputs** (priority field only appears when needed)
- **Concise execution timeline** format

## 🧮 Supported Scheduling Algorithms

<details>
<summary><b>First Come First Serve (FCFS)</b></summary>
<br>
<ul>
  <li>Processes are executed in the order they arrive</li>
  <li>Non-preemptive algorithm</li>
  <li>Simple but can lead to the convoy effect</li>
</ul>
<div align="center">
  <img src="https://media.geeksforgeeks.org/wp-content/uploads/20220525174157/fcfs-660x374.png" width="400">
</div>
</details>

<details>
<summary><b>Shortest Job First (SJF)</b></summary>
<br>
<ul>
  <li>Executes the process with the shortest burst time first</li>
  <li>Non-preemptive algorithm</li>
  <li>Optimal for minimizing average waiting time</li>
</ul>
<div align="center">
  <img src="https://media.geeksforgeeks.org/wp-content/uploads/20220525174158/sjf-660x374.png" width="400">
</div>
</details>

<details>
<summary><b>Round Robin (RR)</b></summary>
<br>
<ul>
  <li>Each process gets a fixed time slice (time quantum)</li>
  <li>Preemptive algorithm</li>
  <li>Good for time-sharing systems</li>
</ul>
<div align="center">
  <img src="https://media.geeksforgeeks.org/wp-content/uploads/20220525174159/rr-660x374.png" width="400">
</div>
</details>

<details>
<summary><b>Priority Scheduling</b></summary>
<br>
<ul>
  <li>Processes are executed based on priority</li>
  <li>Can be preemptive or non-preemptive</li>
  <li>Lower priority value means higher priority</li>
  <li>May lead to starvation of low-priority processes</li>
</ul>
<div align="center">
  <img src="https://media.geeksforgeeks.org/wp-content/uploads/20220525174158/priority-660x374.png" width="400">
</div>
</details>

## 📊 Performance Metrics

<div align="center">
  <img src="https://user-images.githubusercontent.com/74038190/212284158-e840e285-664b-44d7-b79b-e264b5e54825.gif" width="400">
</div>

For each process, the application calculates:

| Metric | Description | Formula |
|--------|-------------|---------|
| **Completion Time** | When the process finishes execution | - |
| **Turnaround Time** | Total time from submission to completion | Completion Time - Arrival Time |
| **Waiting Time** | Time spent waiting in the ready queue | Turnaround Time - Burst Time |

The application also displays average metrics for all processes to help compare algorithm efficiency.

## 🛠️ Installation and Usage

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/cpu-scheduler-simulator.git
cd cpu-scheduler-simulator

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install the required packages
pip install streamlit pandas matplotlib numpy

# Run the application
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📝 How to Use

<div align="center">
  <img src="https://user-images.githubusercontent.com/74038190/235224431-e8c8c12e-6826-47f1-89fb-2ddad83b3abf.gif" width="300">
</div>

### 1. Add Processes
- Simply click on the input fields (they auto-select for easy data entry)
- Enter the Arrival Time, Burst Time, and Priority (if applicable)
- Click "Add Process" to add it to the list
- Repeat for all processes you want to simulate

### 2. Select Algorithm
- Choose a scheduling algorithm from the sidebar dropdown
- For Round Robin, specify the Time Quantum
- For Priority Scheduling, choose whether to use preemption
- The priority input field will only appear when Priority Scheduling is selected

### 3. Run Simulation
- Click "Run Simulation" to execute the selected algorithm
- View the Gantt chart, metrics table, and execution timeline
- The concise timeline format shows process execution in a compact form (e.g., 'P1:0-3,P3:3-6,P1:6-9')

### 4. Modify Processes
- Remove individual processes using the "Remove" button
- Clear all processes using the "Clear All Processes" button

## 📁 Project Structure

```
cpu-scheduler-simulator/
├── app.py                    # Main Streamlit application
├── scheduling_algorithms.py  # Implementation of scheduling algorithms
├── visualization.py          # Functions for creating visualizations
├── requirements.txt          # Required packages
└── README.md                 # Project documentation
```

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgements

<div align="center">
  <img src="https://user-images.githubusercontent.com/74038190/213866269-5d00981c-7c98-46d7-8a8e-16f462f15227.gif" width="200">
</div>

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Matplotlib](https://matplotlib.org/) for visualization capabilities
- [Pandas](https://pandas.pydata.org/) for data manipulation
- This project was created as an educational tool to help understand CPU scheduling algorithms

---

<div align="center">
  <p>Made with ❤️ for Operating Systems enthusiasts</p>
  <p>
    <a href="https://github.com/yourusername">
      <img src="https://img.shields.io/github/followers/yourusername?label=Follow&style=social" alt="GitHub followers">
    </a>
    <a href="https://github.com/yourusername/cpu-scheduler-simulator">
      <img src="https://img.shields.io/github/stars/yourusername/cpu-scheduler-simulator?style=social" alt="GitHub stars">
    </a>
  </p>
</div>

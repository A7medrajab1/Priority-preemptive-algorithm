import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class Process:
    process_count = 0

    @classmethod
    def make_id(cls):
        cls.process_count += 1
        return cls.process_count

    def __init__(self, arrival_time, burst_time, priority):
        self.pid = Process.make_id()
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.time_in = []
        self.temp_burst_time = burst_time
        self.time_out = None
        self.completion_time = None
        self.turnaround_time = None
        self.waiting_time = None
        self.response_time = None

def preemptive(processes):
    all_time = 0
    processes.sort(key=lambda p: p.priority)
    number_of_processes = sum(process.burst_time for process in processes)
    start = 0
    arrival = sorted(process.arrival_time for process in processes)

    gantt_data = []
    while number_of_processes > 0:
        for process in processes:
            if start >= process.arrival_time and process.temp_burst_time > 0:
                process.temp_burst_time -= 1
                process.time_in.append(start)
                process.time_out = start
                start += 1
                gantt_data.append((process.pid, start))
                break
        number_of_processes -= 1
    calculate_average_times(processes)
    return gantt_data


def calculate_average_times(processes):
    total_waiting_time = 0
    total_response_time = 0
    total_turnaround_time = 0
    num_processes = len(processes)

    for process in processes:
        total_turnaround_time += (process.time_out + 1 - process.arrival_time)
        total_waiting_time += ((process.time_out + 1 - process.arrival_time) - process.burst_time)
        total_response_time += (process.time_in[0] - process.arrival_time)

    avg_waiting_time = total_waiting_time / num_processes
    avg_response_time = total_response_time / num_processes
    avg_turnaround_time = total_turnaround_time / num_processes

    messagebox.showinfo("Average Times", 
        f"Average Turnaround Time: {avg_turnaround_time:.2f}\n"
        f"Average Waiting Time: {avg_waiting_time:.2f}\n"
        f"Average Response Time: {avg_response_time:.2f}\n"
    )


def get_process_data():
    num_processes = int(entry_processes.get())
    processes = []
    for i in range(num_processes):
        arrival_time = int(entries_arrival[i].get())
        burst_time = int(entries_burst[i].get())
        priority = int(entries_priority[i].get())
        processes.append(Process(arrival_time, burst_time, priority))
    gantt_data = preemptive(processes)
    draw_gantt_chart(gantt_data)


def draw_gantt_chart(gantt_data):
    fig, ax = plt.subplots()
    ax.set_title('Gantt Chart for Preemptive Priority Scheduling')
    ax.set_xlabel('Time')
    ax.set_ylabel('Process')
    for i, (pid, start) in enumerate(gantt_data):
        ax.add_patch(Rectangle((start - 1, i), 1, 0.5, color='blue', alpha=0.5))
        ax.text(start - 0.5, i + 0.25, f'P{pid}', color='black', ha='center')
    ax.set_ylim(-0.5, len(gantt_data) - 0.5)
    ax.set_xlim(0, gantt_data[-1][1] + 1)
    ax.grid(True)
    plt.show()


def create_process_widgets():
    num_processes = int(entry_processes.get())
    global entries_arrival, entries_burst, entries_priority
    entries_arrival = []
    entries_burst = []
    entries_priority = []
    for i in range(num_processes):
        lbl_arrival = tk.Label(frame_processes, text=f"Arrival Time for Process {i+1}:")
        lbl_arrival.grid(row=i+1, column=0, padx=5, pady=5, sticky="e")
        entry_arrival = tk.Entry(frame_processes, width=10)
        entry_arrival.grid(row=i+1, column=1, padx=5, pady=5)
        entries_arrival.append(entry_arrival)

        lbl_burst = tk.Label(frame_processes, text=f"Burst Time for Process {i+1}:")
        lbl_burst.grid(row=i+1, column=2, padx=5, pady=5, sticky="e")
        entry_burst = tk.Entry(frame_processes, width=10)
        entry_burst.grid(row=i+1, column=3, padx=5, pady=5)
        entries_burst.append(entry_burst)

        lbl_priority = tk.Label(frame_processes, text=f"Priority for Process {i+1}:")
        lbl_priority.grid(row=i+1, column=4, padx=5, pady=5, sticky="e")
        entry_priority = tk.Entry(frame_processes, width=10)
        entry_priority.grid(row=i+1, column=5, padx=5, pady=5)
        entries_priority.append(entry_priority)

    btn_calculate = tk.Button(frame_processes, text="Calculate", command=get_process_data)
    btn_calculate.grid(row=num_processes+1, columnspan=6, pady=10)


# GUI setup
root = tk.Tk()
root.title("Preemptive Priority Scheduling")

frame_processes = tk.Frame(root)
frame_processes.pack(padx=15, pady=15)

lbl_processes = tk.Label(frame_processes, text="Enter the number of processes:")
lbl_processes.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="e")
entry_processes = tk.Entry(frame_processes, width=10)
entry_processes.grid(row=0, column=2, padx=5, pady=5)

btn_create = tk.Button(frame_processes, text="Create Process Entries", command=create_process_widgets)
btn_create.grid(row=0, column=3, padx=5, pady=5)

root.mainloop()

import matplotlib.pyplot as plt

class Process:
    def __init__(self, process_id, arrival_time, burst_time, priority=0):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.start_time = None
        self.end_time = None
        self.remaining_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0

def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)
    time = 0
    for process in processes:
        process.start_time = max(time, process.arrival_time)
        process.end_time = process.start_time + process.burst_time
        process.turnaround_time = process.end_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        time = process.end_time

def sjn_scheduling(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.burst_time))
    time = 0
    ready_queue = []
    while processes or ready_queue:
        ready_queue.extend([p for p in processes if p.arrival_time <= time])
        processes = [p for p in processes if p.arrival_time > time]
        if ready_queue:
            ready_queue.sort(key=lambda x: x.burst_time)
            process = ready_queue.pop(0)
            process.start_time = time
            process.end_time = time + process.burst_time
            process.turnaround_time = process.end_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            time = process.end_time
        else:
            time += 1

def priority_scheduling(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.priority))
    time = 0
    ready_queue = []
    while processes or ready_queue:
        ready_queue.extend([p for p in processes if p.arrival_time <= time])
        processes = [p for p in processes if p.arrival_time > time]
        if ready_queue:
            ready_queue.sort(key=lambda x: x.priority)
            process = ready_queue.pop(0)
            process.start_time = time
            process.end_time = time + process.burst_time
            process.turnaround_time = process.end_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            time = process.end_time
        else:
            time += 1

def round_robin_scheduling(processes, quantum):
    time = 0
    ready_queue = [p for p in processes if p.arrival_time <= time]
    processes = [p for p in processes if p.arrival_time > time]
    while ready_queue or processes:
        if not ready_queue:
            time = processes[0].arrival_time
            ready_queue.append(processes.pop(0))
        process = ready_queue.pop(0)
        process.start_time = time if process.start_time is None else process.start_time
        execution_time = min(process.remaining_time, quantum)
        time += execution_time
        process.remaining_time -= execution_time
        if process.remaining_time == 0:
            process.end_time = time
            process.turnaround_time = process.end_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
        else:
            ready_queue.extend([p for p in processes if p.arrival_time <= time])
            processes = [p for p in processes if p.arrival_time > time]
            ready_queue.append(process)

def calculate_avg_times(processes):
    total_waiting_time = sum(p.waiting_time for p in processes)
    total_turnaround_time = sum(p.turnaround_time for p in processes)
    n = len(processes)
    return total_waiting_time / n, total_turnaround_time / n

def plot_gantt_chart(processes):
    fig, ax = plt.subplots()
    for process in processes:
        ax.barh(f"P{process.process_id}", process.end_time - process.start_time,
                left=process.start_time, color='skyblue')
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart")
    plt.show()

def main():
    processes = [
        Process(1, 0, 8, 2),
        Process(2, 1, 4, 1),
        Process(3, 2, 9, 3),
        Process(4, 3, 5, 2)
    ]
    print("Choose Scheduling Algorithm:")
    print("1. First-Come-First-Serve (FCFS)")
    print("2. Shortest Job Next (SJN)")
    print("3. Priority Scheduling")
    print("4. Round Robin")
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        fcfs_scheduling(processes)
    elif choice == 2:
        sjn_scheduling(processes)
    elif choice == 3:
        priority_scheduling(processes)
    elif choice == 4:
        quantum = int(input("Enter time quantum: "))
        round_robin_scheduling(processes, quantum)
    else:
        print("Invalid choice!")
        return

    avg_waiting_time, avg_turnaround_time = calculate_avg_times(processes)
    print(f"Average Waiting Time: {avg_waiting_time:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround_time:.2f}")
    plot_gantt_chart(processes)

if __name__ == "__main__":
    main()

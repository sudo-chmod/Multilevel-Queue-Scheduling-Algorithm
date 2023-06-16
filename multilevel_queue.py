from collections import deque

class Process:
    def __init__(self, pid, burst_time, priority):
        self.pid = pid
        self.burst_time = burst_time
        self.priority = priority
        self.waiting_time = 0
        self.turnaround_time = 0
        self.remaining_time = burst_time

q0 = deque() #RR
q1 = deque() #SJF
q2 = deque() #SJF
q3 = deque() #FCFS

def GetProcessID(i):
    id = str(i + 1)
    if len(id) == 1:
        return "00" + id
    elif len(id) == 2:
        return "0" + id
    else:
        return id

def FinishingExecution(process, current_time):
    process.turnaround_time = current_time
    process.waiting_time = process.turnaround_time - process.burst_time
    print(f"Process #{process.pid} has finished execution.")
    print(f"Turnaround time\t: {process.turnaround_time}sec")
    print(f"Waiting Time\t: {process.waiting_time}sec\n")
    total_time[process.priority][0] += process.turnaround_time
    total_time[process.priority][1] += process.waiting_time

def RR(queue, current_time, time_limit, time_quentum):
    time = 0
    while (time != time_limit):
        if not queue:
            break
        if time > 15:
            round_time = time_limit - time
        else:
            round_time = time_quentum
        process = queue.popleft()
        if round_time < process.remaining_time:
            current_time += time_quentum
            process.remaining_time -= time_quentum
            queue.append(process)
        else:
            current_time += process.remaining_time
            round_time = process.remaining_time
            process.remaining_time = 0
            FinishingExecution(process,current_time)
        time += round_time
    return current_time
                       
def FCFS(queue, current_time, time_limit):
    time = 0
    while (time != time_limit):
        if not queue:
            break
        process = queue.popleft()
        if (time_limit - time) <= process.remaining_time:
            current_time += (time_limit - time)
            process.remaining_time -= (time_limit - time)
            time = time_limit
            if (time_limit - time) == process.remaining_time:
                FinishingExecution(process,current_time)
            else:
                queue.appendleft(process)
        else:
            time += process.remaining_time
            current_time += process.remaining_time
            process.remaining_time = 0
            FinishingExecution(process,current_time)
    return current_time

def SJF(queue, current_time, time_limit):
    if not queue:
        return current_time
    return FCFS(queue, current_time, time_limit)

print("\n" + "="*38 + "\n")

number_of_process = [0,0,0,0]
for i in range(int(input("Enter the number of processes : "))):
    pid = GetProcessID(i)
    burst_time, priority = map(int, input().split())
    temp = Process(pid, burst_time, priority)
    if priority == 0:
        q0.append(temp)
        number_of_process[0] += 1
    elif priority == 1:
        q1.append(temp)
        number_of_process[1] += 1
    elif priority == 2:
        q2.append(temp)
        number_of_process[2] += 1
    elif priority == 3:
        q3.append(temp)
        number_of_process[3] += 1

current_time = 0
total_time = [[0,0],[0,0],[0,0],[0,0]] #[turnaround_time, waiting_time]
time_limit = 20
time_quentum = 5

q1 = deque(sorted(q1, key=lambda x: x.burst_time))
q2 = deque(sorted(q2, key=lambda x: x.burst_time))

print("\n" + "="*38 + "\n")

while q0 or q1 or q2 or q3:
    current_time = RR(q0, current_time, time_limit, time_quentum)
    current_time = SJF(q1, current_time, time_limit)
    current_time = SJF(q2, current_time, time_limit)
    current_time = FCFS(q3, current_time, time_limit)

print("\n" + "="*38 + "\n")

names = ["Round Robin","Shortest Job First(1)","Shortest Job First(2)","First-In-First-Out"]
for i in range(4):
    if number_of_process[i] == 0:
        continue
    print(f"{names[i]} Queue")
    print("-"*(len(names[i])+6))
    print(f"Avarage Turnaround Time\t= {(total_time[i][0]/number_of_process[i]):.2f}")
    print(f"Avarage Waiting Time\t= {(total_time[i][1]/number_of_process[i]):.2f}\n")

print("\n" + "="*38 + "\n")

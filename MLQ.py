QUEUE_SIZE = 10

class Process:
    def __init__(self, p_id, prio, s_t, b_t):
        self.p_id = p_id
        self.prio = prio
        self.s_t = s_t
        self.b_t = b_t
        self.remain_t = b_t

class Queue:
    def __init__(self):
        self.front = -1
        self.rear = -1
        self.size = 0
        self.queue_array = [None] * QUEUE_SIZE

global globalTime
globalTime = 0

def setQueue(q):
    q.front = -1
    q.rear = -1

def isEmpty(q):
    return q.front == -1

def isFull(q):
    return q.front == (q.rear + 1) % QUEUE_SIZE

def enqueue(q, p1):
    if isFull(q):
        print("Case param! QUEUE IS FULL")
    else:
        if q.front == -1:
            q.front = 0

        q.rear = (q.rear + 1) % QUEUE_SIZE
        q.queue_array[q.rear] = p1
        q.size += 1

def dequeue(q):
    if isEmpty(q):
        print("Case! QUEUE IS EMPTY")

    if (q.front + 1) % QUEUE_SIZE == q.rear:
        p_return = q.queue_array[q.front]
        q.front = -1
        q.rear = -1
        return p_return

    p_return = q.queue_array[q.front]
    q.front = (q.front + 1) % QUEUE_SIZE
    return p_return

def print_queue(q):
    print()
    for process in q.queue_array:
        if process is not None:
            print("Process ID: ", process.p_id, "Priority ID: ", process.prio, "Burst Time: ", process.b_t)
    print()

def input_processes():
    noOfProcess = int(input("Enter the number of processes: "))
    q0 = Queue()
    setQueue(q0)

    for i in range(noOfProcess):
        p = Process(0, 0, 0, 0)
        p.p_id = int(input("Enter Process ID: "))
        p.prio = int(input("Enter Priority ID: "))
        p.b_t = int(input("Enter Burst Time: "))
        p.remain_t = p.b_t

        if p.prio == 0:
            enqueue(q0, p)

    return q0

def fcfs(q0):
    global globalTime
    quantum_slice = 4
    print("The global time is", globalTime)
    
    # Execute the loop at least once
    while (quantum_slice != 0):
        for i in range(q0.size):

            if q0.queue_array[i].b_t != 0 and q0.queue_array[i].b_t <= quantum_slice:
                q0.size -= 1
                quantum_slice -= q0.queue_array[i].b_t
                globalTime += q0.queue_array[i].b_t
                print("Process", q0.queue_array[i].p_id, "exited at time", globalTime)

                dequeue(q0)
            elif q0.queue_array[i].b_t != 0 and q0.queue_array[i].b_t > quantum_slice:
                q0.queue_array[i].b_t -= quantum_slice
                globalTime += quantum_slice
        
        # Break the loop if the condition is met
        # if globalTime % quantum_slice == 0 or q0.size == 0:
        #     break
    


def schedule():
    global globalTime
    no_queues = 2
    tick = 0
    quantum_slice = 4

    while globalTime < 12:

        if globalTime % (no_queues * quantum_slice) == 0:
            tick += 1

        if tick % no_queues == 0: # a switch is supposed to happen
            globalTime += quantum_slice - 1
        
        else:
            fcfs(q0)



q0 = input_processes()
print_queue(q0)
schedule()

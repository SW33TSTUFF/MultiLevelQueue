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
    
    else:
        p_return = q.queue_array[q.front]
        q.front = (q.front + 1) % QUEUE_SIZE
        q.size -= 1
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
    q1 = Queue()
    setQueue(q1)

    for i in range(noOfProcess):
        p = Process(0, 0, 0, 0)
        p.p_id = int(input("Enter Process ID: "))
        p.prio = int(input("Enter Priority ID: "))
        p.b_t = int(input("Enter Burst Time: "))
        p.remain_t = p.b_t

        if p.prio == 0:
            enqueue(q0, p)
        elif p.prio == 1:
            enqueue(q1, p)


    return q0, q1

def fcfs(q0):
    global globalTime
    quantum_slice = 2
    print("The global time is", globalTime)
    
    # Execute the loop at least once
    while (quantum_slice != 0):
        initial_size = q0.size
        initial_front = q0.front
        for i in range(initial_size):

            if (quantum_slice == 0):
                break

            if q0.queue_array[i + initial_front].b_t != 0 and q0.queue_array[i + initial_front].b_t <= quantum_slice:
                quantum_slice -= q0.queue_array[i + initial_front].b_t
                globalTime += q0.queue_array[i + initial_front].b_t
                q0.queue_array[i + initial_front].b_t = 0
                print("Process", q0.queue_array[i + initial_front].p_id, "exited at time", globalTime)

                dequeue(q0)
            elif q0.queue_array[i + initial_front].b_t != 0 and q0.queue_array[i + initial_front].b_t > quantum_slice:
                q0.queue_array[i + initial_front].b_t -= quantum_slice
                globalTime += quantum_slice
                quantum_slice = 0


def roundrobin(q0):
    global globalTime
    quantum_slice = 8
    robin_slice = 4
    print("The global time is", globalTime)
    
    # Execute the loop at least once
    while (quantum_slice != 0):
        initial_size = q0.size
        initial_front = q0.front
        robin_slice = 4
        for i in range(initial_size):

            if (quantum_slice == 0):
                break

            if (quantum_slice != 0 and robin_slice == 0):
                break

            diff = abs(quantum_slice - robin_slice)

            if (quantum_slice >= robin_slice):
                if q1.queue_array[i + initial_front].b_t != 0 and q1.queue_array[i + initial_front].b_t <= robin_slice:
                    quantum_slice -= q1.queue_array[i + initial_front].b_t
                    robin_slice -= q1.queue_array[i + initial_front].b_t
                    globalTime += q1.queue_array[i + initial_front].b_t
                    q1.queue_array[i + initial_front].b_t = 0
                    print("Process", q1.queue_array[i + initial_front].p_id, "exited at time", globalTime)

                    dequeue(q1)

                elif q1.queue_array[i + initial_front].b_t != 0 and q1.queue_array[i + initial_front].b_t > robin_slice:
                    q1.queue_array[i + initial_front].b_t -= robin_slice
                    globalTime += robin_slice
                    quantum_slice -= robin_slice
                    robin_slice = 0
            
            elif (robin_slice > quantum_slice):
                if q1.queue_array[i + initial_front].b_t != 0 and q1.queue_array[i + initial_front].b_t <= quantum_slice:
                    quantum_slice -= q1.queue_array[i + initial_front].b_t
                    robin_slice -= q1.queue_array[i + initial_front].b_t
                    globalTime += q1.queue_array[i + initial_front].b_t
                    q1.queue_array[i + initial_front].b_t = 0
                    print("Process", q1.queue_array[i + initial_front].p_id, "exited at time", globalTime)

                    dequeue(q1)
                elif q1.queue_array[i + initial_front].b_t != 0 and q1.queue_array[i + initial_front].b_t > quantum_slice:
                    q1.queue_array[i + initial_front].b_t -= quantum_slice
                    # Dont need to account for robin_slice from this point 
                    globalTime += quantum_slice
                    quantum_slice = 0

            # we need 2 conditions, we need the absolute value of rr slice and quantum slice


def schedule():
    global globalTime
    no_queues = 2
    tick = 0
    quantum_slice = 8
    switch_count = 0

    while (globalTime < 25):
        if (switch_count == 0):
            # fcfs(q0)
            roundrobin(q1)
        elif (switch_count == 1):
            globalTime += quantum_slice
        switch_count = (switch_count + 1) % 2



q0, q1 = input_processes()
print_queue(q0)
print_queue(q1)
schedule()

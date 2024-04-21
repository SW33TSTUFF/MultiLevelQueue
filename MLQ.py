QUEUE_SIZE = 200

class Process:
    def __init__(self, p_id, prio, s_t, b_t):
        self.p_id = p_id
        self.prio = prio
        self.s_t = s_t
        self.b_t = b_t
        self.remain_t = b_t
        self.finish_t = 0
        self.start_t = 0

class Queue:
    def __init__(self):
        self.front = -1
        self.rear = -1
        self.size = 0
        self.queue_array = [None] * QUEUE_SIZE

global globalTime
globalTime = 0

global emptyFlag
emptyFlag = [0,0,0,0]


def setQueue(q):
    q.front = -1
    q.rear = -1

def isEmpty(q):
    return q.front == -1

def isFull(q):
    return q.front == (q.rear + 1) % QUEUE_SIZE

def enqueue(q, p1):
    if isFull(q):
        print("QUEUE IS FULL")
    else:
        if q.front == -1:
            q.front = 0

        q.rear = (q.rear + 1) % QUEUE_SIZE
        q.queue_array[q.rear] = p1
        q.size += 1

def dequeue(q):
    global globalTime
    if isEmpty(q):
        print("QUEUE IS EMPTY")
    
    if (q.front == q.rear):
        p_return = q.queue_array[q.front]
        p_return.finish_t = globalTime
        q.queue_array[q.front] = None
        q.front == -1
        q.rear == -1
        q.size -= 1
        enqueue(finished_queue, p_return)
        return p_return
    else:
        p_return = q.queue_array[q.front]
        p_return.finish_t = globalTime
        q.queue_array[q.front] = None
        q.front = (q.front + 1) % QUEUE_SIZE
        q.size -= 1
        enqueue(finished_queue, p_return)
        return p_return
    
def robin_dequeue(q):
    if isEmpty(q):
        print("Case! QUEUE IS EMPTY")
    
    else:
        p_return = q.queue_array[q.front]
        enqueue(q, p_return)
        q.queue_array[q.front] = None
        q.front = (q.front + 1) % QUEUE_SIZE
        q.size -= 1

def print_queue(q):
    print()
    for process in q.queue_array:
        if process is not None:
            print("Process ID: ", process.p_id, 
                  "Priority ID: ", process.prio, 
                  "Burst Time: ", process.b_t)
    print()

def print_finish_queue(q):
    print()
    for i in range(4):
        print("PRIORITY", i)
        for process in q.queue_array:
            if process is not None and process.prio == i:
                print("P ID: ", process.p_id, 
                    #"\tPriority ID: ", process.prio, 
                    "\tBT: ", process.b_t, 
                    "\tCompT: ", process.finish_t, 
                    "\tTurnT: ", process.finish_t - process.s_t, 
                    "\tWaitT: ", process.finish_t - process.s_t - process.b_t)
        print()

    print()
    print("PROCESS EXECUTION ORDER ", end='')
    process_ids = []
    for process in q.queue_array:
        if process is not None:
            process_ids.append("P" + str(process.p_id))
    print(", ".join(process_ids))





def process_init():
    noOfProcess = int(input("Enter the number of processes: "))
    print()
    q0 = Queue()
    setQueue(q0)
    q1 = Queue()
    setQueue(q1)
    q2 = Queue()
    setQueue(q2)
    q3 = Queue()
    setQueue(q3)
    finished_queue = Queue()
    setQueue(finished_queue)

    for i in range(noOfProcess):
        p = Process(0, 0, 0, 0)
        p.p_id = int(input("Enter Process ID: "))
        p.prio = int(input("Enter Priority ID: "))
        p.b_t = int(input("Enter Burst Time: "))
        print()
        p.remain_t = p.b_t

        if p.prio == 0:
            enqueue(q0, p)
        elif p.prio == 1:
            enqueue(q1, p)
        elif p.prio == 2:
            enqueue(q2, p)
        elif p.prio == 3:
            enqueue(q3, p)


    return q0, q1, q2, q3, finished_queue



def roundrobin(q0):
    if (q0.size == 0):
        #print("q0 is now empty")
        emptyFlag[0] = 1
        return
    
    global globalTime
    quantum_slice = 20
    robin_slice = int(quantum_slice/q0.size)
    #print("The global time is", globalTime)
    
    # Execute the loop at least once
    while (quantum_slice != 0):
        initial_size = q0.size
        initial_front = q0.front

        if (q0.size == 0):
            break
        
        for i in range(initial_size):

            if (quantum_slice == 0 or q0.size == 0):
                break

            if (quantum_slice != 0 and robin_slice == 0):
                if (quantum_slice > q0.size):
                    robin_slice = int(quantum_slice/q0.size)
                else:
                    robin_slice = quantum_slice


            if (quantum_slice >= robin_slice):
                if q0.queue_array[i + initial_front].remain_t != 0 and q0.queue_array[i + initial_front].remain_t <= robin_slice:
                    quantum_slice -= q0.queue_array[i + initial_front].remain_t
                    # robin_slice -= q0.queue_array[i + initial_front].remain_t
                    robin_slice = 4 # if the jobs done we can simply reset the robin_slice
                    globalTime += q0.queue_array[i + initial_front].remain_t
                    q0.queue_array[i + initial_front].remain_t = 0
                    print("Process", q0.queue_array[i + initial_front].p_id, "exited at time", globalTime)

                    dequeue(q0)

                elif q0.queue_array[i + initial_front].remain_t != 0 and q0.queue_array[i + initial_front].remain_t > robin_slice:
                    q0.queue_array[i + initial_front].remain_t -= robin_slice
                    globalTime += robin_slice
                    quantum_slice -= robin_slice
                    robin_slice = 0
                    robin_dequeue(q0)
            
            elif (robin_slice > quantum_slice):
                if q0.queue_array[i + initial_front].remain_t != 0 and q0.queue_array[i + initial_front].remain_t <= quantum_slice:
                    quantum_slice -= q0.queue_array[i + initial_front].remain_t
                    robin_slice -= q0.queue_array[i + initial_front].remain_t
                    globalTime += q0.queue_array[i + initial_front].remain_t
                    q0.queue_array[i + initial_front].remain_t = 0
                    print("Process", q0.queue_array[i + initial_front].p_id, "exited at time", globalTime)

                    dequeue(q0)
                elif q0.queue_array[i + initial_front].remain_t != 0 and q0.queue_array[i + initial_front].remain_t > quantum_slice:
                    q0.queue_array[i + initial_front].remain_t -= quantum_slice
                    # Dont need to account for robin_slice from this point 
                    globalTime += quantum_slice
                    quantum_slice = 0
                    # enqueue(q0, dequeue(q1))


def sjf_1(q1):

    if (q1.size == 0):
        #print("q1 is now empty")
        emptyFlag[1] = 1
        return

    global globalTime
    quantum_slice = 20
    #print("The global time is", globalTime)

    while (quantum_slice != 0):

        if (q1.size == 0):
            break
        initial_size = q1.size
        initial_front = q1.front

        set_min = q1.queue_array[q1.front].remain_t
        set_index = 0
        for k in range(q1.front, q1.front + q1.size):
            if (q1.queue_array[k].remain_t <= set_min):
                set_min = q1.queue_array[k].remain_t
                set_index = k

        if (initial_front == set_index):    
            if (quantum_slice == 0 or q1.size == 0):
                break

            if q1.queue_array[set_index].remain_t != 0 and q1.queue_array[set_index].remain_t <= quantum_slice:
                quantum_slice -= q1.queue_array[set_index].remain_t
                globalTime += q1.queue_array[set_index].remain_t
                q1.queue_array[set_index].remain_t = 0
                print("Process", q1.queue_array[set_index].p_id, "exited at time", globalTime)

                dequeue(q1)
            elif q1.queue_array[set_index].remain_t != 0 and q1.queue_array[set_index].remain_t > quantum_slice:
                q1.queue_array[set_index].remain_t -= quantum_slice
                globalTime += quantum_slice
                quantum_slice = 0

        else:
            robin_dequeue(q1)

def sjf_2(q2):

    if (q2.size == 0):
        #print("q2 is now empty")
        emptyFlag[2] = 1
        return
    
    global globalTime
    quantum_slice = 20
    #print("The global time is", globalTime)

    while (quantum_slice != 0):

        if (q2.size == 0):
            break
        initial_size = q2.size
        initial_front = q2.front

        set_min = q2.queue_array[q2.front].remain_t
        set_index = 0
        for k in range(q2.front, q2.front + q2.size):
            if (q2.queue_array[k].remain_t <= set_min):
                set_min = q2.queue_array[k].remain_t
                set_index = k

        if (initial_front == set_index or q2.size == 0):    
            if (quantum_slice == 0):
                break

            if q2.queue_array[set_index].remain_t != 0 and q2.queue_array[set_index].remain_t <= quantum_slice:
                quantum_slice -= q2.queue_array[set_index].remain_t
                globalTime += q2.queue_array[set_index].remain_t
                q2.queue_array[set_index].remain_t = 0
                print("Process", q2.queue_array[set_index].p_id, "exited at time", globalTime)

                dequeue(q2)
            elif q2.queue_array[set_index].remain_t != 0 and q2.queue_array[set_index].remain_t > quantum_slice:
                q2.queue_array[set_index].remain_t -= quantum_slice
                globalTime += quantum_slice
                quantum_slice = 0

        else:
            robin_dequeue(q2)

def fifo(q3):
    global emptyFlag
    if (q3.size == 0):
        #print("q3 is now empty")
        emptyFlag[3] = 1
        return

    global globalTime
    quantum_slice = 20
    #print("The global time is", globalTime)
    
    while (quantum_slice != 0):
        if (q3.size == 0):
            break
        
        initial_size = q3.size
        initial_front = q3.front
        for i in range(initial_size):

            if (quantum_slice == 0):
                break

            if q3.queue_array[i + initial_front].remain_t != 0 and q3.queue_array[i + initial_front].remain_t <= quantum_slice:
                quantum_slice -= q3.queue_array[i + initial_front].remain_t
                globalTime += q3.queue_array[i + initial_front].remain_t
                q3.queue_array[i + initial_front].remain_t = 0
                print("Process", q3.queue_array[i + initial_front].p_id, "exited at time", globalTime)

                dequeue(q3)
            elif q3.queue_array[i + initial_front].remain_t != 0 and q3.queue_array[i + initial_front].remain_t > quantum_slice:
                q3.queue_array[i + initial_front].remain_t -= quantum_slice
                globalTime += quantum_slice
                quantum_slice = 0



def multilevel():
    global globalTime
    global emptyFlag
    no_queues = 4
    switch_count = 0

    while (globalTime < 10000):

        if (emptyFlag[0] == 1 and emptyFlag[1] == 1 and emptyFlag[2] == 1 and emptyFlag[3] == 1):
            print()
            print("END OF EXECUTION")
            print()
            print_finish_queue(finished_queue)
            break

        elif (switch_count == 0 and emptyFlag[0] != 1):
            roundrobin(q0)
            
        elif (switch_count == 1 and emptyFlag[1] != 1):
            sjf_1(q1)

        elif (switch_count == 2 and emptyFlag[2] != 1):
            sjf_2(q2)

        elif (switch_count == 3 and emptyFlag[3] != 1):
            fifo(q3)
        switch_count = (switch_count + 1) % no_queues



q0, q1, q2, q3, finished_queue = process_init()
print_queue(q0)
print_queue(q1)
print_queue(q2)
print_queue(q3)
multilevel()

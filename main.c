#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#define QUEUE_SIZE 20

struct process {
    int p_id;
    int priority;
    int burst_time;
    int wait_time;
    int turnaround_time;
};

struct queue {
    int front;
    int rear;
    struct process Processes[QUEUE_SIZE];
};

void setQueue(struct queue *q);
bool isEmpty(struct queue *q);
bool isFull(struct queue *q);
void enqueue(struct queue *q, struct process p);
void dequeue(struct queue *q);



void multiLevelQueue(struct process* q0, struct process* q1, struct process* q2, struct process* q3);

int main() {

    // Enter process
    int process_count = 0;
    printf("Enter number of proceses: ");
    scanf("%d", &process_count);

    struct process Process[process_count]; // Taking a static value for simpler implementation
    // The user needs to enter the process_id, process priority and process burst time.
    for(int i=0; i < process_count; i++) {
        printf("\nEnter process_id : ");
        scanf("%d", Process[i].p_id);
        printf("\nEnter priority : ");
        scanf("%d", Process[i].priority);
        printf("\nEnter process_id : ");
        scanf("%d", Process[i].burst_time);

    }
    

    printf("Hello!");
    return 0;
}


void setQueue(struct queue *q) {
    q->front = -1;
    q->rear =  -1;
}

bool isEmpty(struct queue *q) {
    if (q->front == -1) {
        return true;
    }
}

bool isFull(struct queue *q) {
    if (q->front == (q->rear +1) % QUEUE_SIZE) {
        return true;
    }
}
void enqueue(struct queue *q, struct process p1) {
    if (isFull(q)) {
        printf("Case param!");
    }
    else {
        if (q->front == - 1) {
            q->front = 0;
        }

        q->rear =  (q->rear + 1) % QUEUE_SIZE;
        q->Processes[q->rear] = p1; 
    
    }
}
void dequeue(struct queue *q);
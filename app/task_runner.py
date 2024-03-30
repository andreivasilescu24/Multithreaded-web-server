from asyncio import Semaphore
from queue import Queue
from threading import Thread, Event, Lock
import time
import os
import random

class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        self.task_queue = Queue()
        self.job_status = {}
        self.job_question = {}
        self.shutdown_event = Event()
        self.job_lock = Lock()

        if os.environ.get('TP_NUM_OF_THREADS') is not None:
            self.num_threads = int(os.environ.get('TP_NUM_OF_THREADS'))
        else:
            self.num_threads = os.cpu_count()
        
        print(f'Number of threads: {self.num_threads}')
        self.my_threads = [TaskRunner(i, self.job_lock, self.task_queue, self.job_status, self.job_question, self.shutdown_event) for i in range(self.num_threads)]
        self.job_id_cnt = 1

        for thread in self.my_threads:
            thread.start()

    def check_job_id(self, job_id):
        if job_id in self.job_status:
            return self.job_status[job_id]
        return None

    def add_task(self, question):
        # Add a task to the queue
        if not self.shutdown_event.is_set():
            print(f'Adding task with job id {self.job_id_cnt}')
            self.task_queue.put(self.job_id_cnt)
            self.job_status[self.job_id_cnt] = 'running'
            self.job_question[self.job_id_cnt] = question
            return self.job_id_cnt
        else:
            return None
    
    def update_job_id(self):
        self.job_id_cnt += 1

    def get_job_status(self, job_id):
        return self.job_status[job_id]
    
    def get_jobs(self):
        with self.job_lock:
            return self.job_status
        
    def is_shutdown_event_set(self):
        return self.shutdown_event.is_set()

    def shutdown(self):
        self.shutdown_event.set()
        for thread in self.my_threads:
            thread.join()
    

class TaskRunner(Thread):
    def __init__(self, tid, lock, task_queue, job_status, jobs_questions, shutdown_event):
        # TODO: init necessary data structures
        Thread.__init__(self)
        self.tid = tid
        self.lock = lock
        self.task_queue = task_queue
        self.job_status = job_status
        self.jobs_questions = jobs_questions
        self.shutdown_event = shutdown_event
        self.job_id = None
        pass

    def run(self):
        print(f'Starting thread {self.tid}')
        while not self.shutdown_event.is_set() or not self.task_queue.empty():
            # TODO
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            if self.task_queue.empty():
                continue
            else:
                self.job_id = self.task_queue.get()
            
            print(f'Thread {self.tid}: Running task with job id {self.job_id}')
            
            time.sleep(random.randint(1, 5))
            
            #TODO: Run the task handler
            self.job_status[self.job_id] = 'done'

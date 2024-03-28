from asyncio import Semaphore
from queue import Queue
from threading import Thread, Event, Lock
import time
import os

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

        if os.environ.get('TP_NUM_OF_THREADS') is not None:
            self.num_threads = int(os.environ.get('TP_NUM_OF_THREADS'))
        else:
            self.num_threads = os.cpu_count()
        
        self.get_task_lock = Lock()
        self.sem = Semaphore(self.num_threads)
        
        self.my_threads = [TaskRunner(self.get_task_lock, self.task_queue) for i in range(self.num_threads)]
        self.job_id_cnt = 1

        for thread in self.my_threads:
            thread.start()

    def check_job_id(self, job_id):
        # print(self.jobs_status[job_id])
        if job_id in self.job_status:
            return self.job_status[job_id]
        return None

    def add_task(self, question):
        # Add a task to the queue
        print(f'Adding task with job id {self.job_id_cnt}')
        self.task_queue.put(self.job_id_cnt)
        self.job_status[self.job_id_cnt] = 'running'
        self.job_question[self.job_id_cnt] = question
        print(self.job_status)
        print(self.job_question)
        return self.job_id_cnt
    
    def update_job_id(self):
        self.job_id_cnt += 1
        print(f'Updating job id to {self.job_id_cnt}')


    def get_job_status(self, job_id):
        # Return the status of a job
        return self.job_status[job_id]

    

class TaskRunner(Thread):
    def __init__(self, lock, task_queue):
        # TODO: init necessary data structures
        Thread.__init__(self)
        self.lock = lock
        self.task_queue = task_queue
        self.job_id = -1
        pass

    def run(self):
        while True:
            # TODO
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            self.job_id = -1
            with self.lock:
                if self.task_queue.empty():
                    break
                else:
                    self.job_id = self.task_queue.get()

            # if job is not None:
            #     # Execute the job
            #     pass
            # else:
            #     break


            pass

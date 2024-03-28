from queue import Queue
from threading import Thread, Event, Lock
import time
import os

class ThreadPool:
    def __init__(self, lock):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        self.task_queue = Queue()

        if os.environ.get('TP_NUM_OF_THREADS') is not None:
            self.num_threads = int(os.environ.get('TP_NUM_OF_THREADS'))
        else:
            self.num_threads = os.cpu_count()
        
        self.lock = lock
        self.my_threads = [TaskRunner(self.lock) for i in range(self.num_threads)]

        

class TaskRunner(Thread):
    def __init__(self, lock):
        # TODO: init necessary data structures
        super().__init__()
        self.lock = lock
        pass

    def run(self):
        while True:
            # TODO
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            pass

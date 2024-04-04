from asyncio import Semaphore
from queue import Queue
from threading import Thread, Event, Lock

import time
import os
import random
import json
from venv import logger


class ThreadPool:
    def __init__(self, data_ingestor, logger):
        self.data_ingestor = data_ingestor
        self.logger = logger
        self.task_queue = Queue()
        self.job_status = {}
        self.job_json = {}
        self.job_type = {}
        self.shutdown_event = Event()
        self.job_lock = Lock()

        if os.environ.get('TP_NUM_OF_THREADS') is not None:
            self.num_threads = int(os.environ.get('TP_NUM_OF_THREADS'))
        else:
            self.num_threads = os.cpu_count()
        
        print(f'Number of threads: {self.num_threads}')
        self.my_threads = [TaskRunner(i, self.job_lock, self.task_queue, self.job_status, self.job_json, self.job_type, self.shutdown_event, self.data_ingestor) 
                           for i in range(self.num_threads)]
        self.job_id_cnt = 1

        for thread in self.my_threads:
            thread.start()

    def check_job_id(self, job_id):
        if job_id in self.job_status:
            return self.job_status[job_id]
        return None

    def add_task(self, json_req, task_type):
        # Add a task to the queue
        if not self.shutdown_event.is_set():
            print(f'Adding task with job id {self.job_id_cnt}')
            self.task_queue.put(self.job_id_cnt)
            with self.job_lock:
                self.job_status[self.job_id_cnt] = 'running'
                self.job_json[self.job_id_cnt] = json_req
                self.job_type[self.job_id_cnt] = task_type

            return self.job_id_cnt
        else:
            return None
    
    def update_job_id(self):
        self.job_id_cnt += 1

    def get_job_status(self, job_id):
        with self.job_lock:
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
        self.logger.info('Server successfully shut down')
    

class TaskRunner(Thread):
    def __init__(self, tid, lock, task_queue, job_status, job_json, job_type, shutdown_event, data_ingestor):
        # TODO: init necessary data structures
        Thread.__init__(self)
        self.tid = tid
        self.lock = lock
        self.task_queue = task_queue
        self.job_status = job_status
        self.job_json = job_json
        self.job_type = job_type
        self.shutdown_event = shutdown_event
        self.job_id = None
        self.data_ingestor = data_ingestor
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
            
            # time.sleep(random.randint(1, 5))
            result = eval('self.data_ingestor.' + self.job_type[self.job_id])(self.job_json[self.job_id])
            with open(f'results/{self.job_id}.json', 'w') as result_file:
                result_file.write(json.dumps(result))

            #TODO: Run the task handler
            with self.lock:
                self.job_status[self.job_id] = 'done'
                print(f'Thread {self.tid}: Task with job id {self.job_id} done')

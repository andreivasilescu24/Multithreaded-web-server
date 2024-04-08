from queue import Queue
import queue
from threading import Thread, Event, Lock

import os
import json

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

        self.my_threads = [TaskRunner(self.job_lock, self.task_queue, self.job_status,
                                      self.job_json, self.job_type, self.shutdown_event,
                                      self.data_ingestor) for _ in range(self.num_threads)]
        self.job_id_cnt = 1

        for thread in self.my_threads:
            thread.start()

    def check_job_id(self, job_id):
        """
        Check the status of a job based on its ID.

        Args:
            job_id (str): The ID of the job to check.

        Returns:
            str or None: The status of the job if it exists, otherwise None.
        """
        with self.job_lock:
            if job_id in self.job_status:
                return self.job_status[job_id]
            return None

    def add_task(self, json_req, task_type):
        """
        Adds a task to the task queue.

        Parameters:
        - json_req (dict): The JSON request for the task.
        - task_type (str): The type of the task.

        Returns:
        - int: The ID of the added task.

        If the shutdown event is not set, the task is added to the task queue with a unique ID.
        The job status, JSON request, and task type are updated in their respective dictionaries.

        If the shutdown event is set, None is returned.
        """
        if not self.shutdown_event.is_set():
            self.task_queue.put(self.job_id_cnt)
            with self.job_lock:
                self.job_status[self.job_id_cnt] = 'running'
                self.job_json[self.job_id_cnt] = json_req
                self.job_type[self.job_id_cnt] = task_type

            return self.job_id_cnt
        return None

    def update_job_id(self):
        self.job_id_cnt += 1

    def get_job_status(self, job_id):
        """
        Retrieve the status of a job.

        Parameters:
        - job_id (int): The ID of the job.

        Returns:
        - str: The status of the job.
        """
        with self.job_lock:
            return self.job_status[job_id]

    def get_jobs(self):
        """
        Returns the current status of the jobs.

        Returns:
            list: A list containing the status of the jobs.
        """
        with self.job_lock:
            return self.job_status

    def is_shutdown_event_set(self):
        """
        Check if the shutdown event is set.

        Returns:
            bool: True if the shutdown event is set, False otherwise.
        """
        return self.shutdown_event.is_set()

    def shutdown(self):
        """
        Shuts down the server by setting the shutdown event, joining all threads,
        and logging a success message.
        """
        self.shutdown_event.set()
        for thread in self.my_threads:
            thread.join()
        self.logger.info('Server successfully shut down')


class TaskRunner(Thread):
    def __init__(self, lock, task_queue, job_status, job_json, job_type,
                 shutdown_event, data_ingestor):
        Thread.__init__(self)
        self.lock = lock
        self.task_queue = task_queue
        self.job_status = job_status
        self.job_json = job_json
        self.job_type = job_type
        self.shutdown_event = shutdown_event
        self.job_id = None
        self.data_ingestor = data_ingestor

    def run(self):
        """
        Executes the thread.

        This method continuously retrieves jobs from the task queue and processes them.
        If the task queue is empty, it waits for a specified timeout period.
        If the shutdown event is set, the method breaks out of the loop and stops execution.
        """
        while True:
            try:
                self.job_id = self.task_queue.get(timeout=2)
            except queue.Empty:
                if self.shutdown_event.is_set():
                    break
                continue

            result = eval('self.data_ingestor.' +
                            self.job_type[self.job_id])(self.job_json[self.job_id])
            with open(f'results/{self.job_id}.json', 'w') as result_file:
                result_file.write(json.dumps(result))

            with self.lock:
                self.job_status[self.job_id] = 'done'

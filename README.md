# Statistical Analysis Web Server

## 1. Solution

The implemented solution will create a Flask server, along with a `DataIngestor` and a `ThreadPool`. As requests are received on the endpoints defined in the assignment, the corresponding handler functions will send the incoming task to the `ThreadPool` if the requests are POST. In the case of GET requests, no new job ID will be created, and no job will be added to the queue, since the request either requires a result from the current moment (e.g., status of the jobs in the `ThreadPool`, the number of jobs in "running," or the result of a job), or the server needs to be shut down, which means the `ThreadPool` will no longer accept new tasks. Thus, only requests that require statistical calculations will generate a job ID and add a task to the queue, allowing us to retrieve job statuses or the number of running jobs, even after the server shuts down, as the `ThreadPool` will continue to execute all remaining tasks in the queue.

Upon receiving a new job, the server will return a JSON response with the new job ID and increment the job ID for the next task. The `ThreadPool` will add the task to its queue, from where a thread can access and execute it, writing the result to the corresponding JSON file named after the job that was executed. This file-based approach for storing results was used to avoid keeping large amounts of data in structures like dictionaries/lists and to make it easier to access the results by reading the content of the file when a request is received to retrieve the result of a particular job.

I consider this assignment useful because it helped consolidate concepts related to multithreaded servers, as well as synchronization mechanisms and their importance in such applications. Additionally, this application is valuable because it provides statistics for large datasets in a reasonable time. I believe the solution is efficient, as threads run tasks in parallel, optimizing the server. Furthermore, the results are stored in files instead of in data structures within the `ThreadPool`, preventing excessive memory usage that could affect efficiency.

## 2. Implementation

I fully implemented the assignment requirements.

In the `ThreadPool`, I keep information about each job that enters the execution queue, using three dictionaries. Each job ID (the key) has associated values such as its status, the JSON content from the request (which will be passed to the statistical functions), and the job type ("states_mean", "global_mean", etc.) to allow each thread to know which function to call to compute the result. In addition to the job queue and these dictionaries, the `ThreadPool` also maintains a list of created threads, an event for server shutdown, and a lock to prevent concurrent access to dictionaries for specific jobs (for example, when a GET request for job status is received, the lock is used on the dictionary to ensure that the status is not updated by another thread while being accessed). All these data structures and synchronization mechanisms are passed as parameters to each thread, enabling them to use them.

When a shutdown is requested, the event is set, notifying all threads that the server is about to close and that they should complete their tasks as quickly as possible once no jobs remain in the queue. The `shutdown` function in the `ThreadPool` will wait for all threads to finish before closing.

Each thread in the `ThreadPool` will continue running until a shutdown is requested and the job queue is empty. A thread tries to pick a job from the queue and execute it, but it will not block for more than 2 seconds. If the queue is empty, it will check if a shutdown has been requested, and if so, the thread will close. I created this mechanism because there is a case where the server starts and immediately requests a shutdown. If all threads were blocked waiting for a task, they would run indefinitely even after the server has closed, and no new tasks will be added. When a thread successfully retrieves a task, it calls the appropriate statistical function based on the job type and writes the result to a JSON file. I used `eval` to dynamically call the corresponding function based on the job type, which is stored in the dictionary in the `ThreadPool` and updated each time a new task is added. After writing the result to the file, the thread updates the status of the job ID to "done" using a lock on the shared status dictionary.

The functions that calculate the results and operate on the received CSV (e.g., "states_mean," "mean_by_category," etc.) are located in the `DataIngestor` to easily access the CSV table. The results of operations on the CSV are obtained using operations provided by the `pandas` library, as it is easy to use and efficient for large datasets like the one used in this assignment. The statistical calculation functions have the same names as the request types they handle, which allows them to be called dynamically using `eval` from within the threads.

Additionally, I created a logging function to monitor server activity. All requests made to the server are logged in the "webserver.log" file, along with a timestamp, the endpoint of the request, and a descriptive message for the action performed. The server's startup and shutdown are also logged, as well as errors such as attempts to add tasks after shutdown.

I created unit tests for the results returned by the statistical functions in `DataIngestor` to validate their correctness. However, these tests run on a much smaller CSV than the one used by the server.

### Resources Used

- https://ocw.cs.pub.ro/courses/asc/laboratoare/02
- https://ocw.cs.pub.ro/courses/asc/laboratoare/03
- https://docs.python.org/3/library/unittest.html#organizing-test-code
- https://docs.python.org/3/library/logging.html
- https://stackoverflow.com/questions/24722212/python-cant-find-module-in-the-same-folder
- https://www.toppr.com/guides/python-guide/references/methods-and-functions/methods/built-in/eval/python-eval/
- https://docs.python.org/3/library/queue.html

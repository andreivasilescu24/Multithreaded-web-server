from crypt import methods
from app import webserver
from flask import request, jsonify

import os
import json
import time

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    print(f"JobID is {job_id}")

    job_id_status = webserver.tasks_runner.check_job_id(int(job_id))
    if job_id_status is not None:
        return jsonify({"status" : job_id_status})
    else: 
        return jsonify({"status": "error", "reason" : "Invalid job_id"})
    # TODO
    # Check if job_id is valid

    # Check if job_id is done and return the result
    #    res = res_for(job_id)
    #    return jsonify({
    #        'status': 'done',
    #        'data': res
    #    })

    # If not, return running status
    # return jsonify({'status': 'NotImplemented'})

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    # Get request data
    # print(f'Current job is {webserver.tasks_runner.job_id_cnt}')
    
    # TODO
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    # webserver.tasks_runner.add_task(webserver.job_counter)
    data = request.json
    print(f"Got request {data}")
    job_id = webserver.tasks_runner.add_task(data['question'])
    
    if job_id is None:
        return jsonify({"status": "error", "reason": "Cannot add task, shutdown was requested"})
    
    webserver.tasks_runner.update_job_id()
    
    return jsonify({"job_id_" + str(job_id) : job_id})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown_request():
    print("Shutting down the server")
    webserver.tasks_runner.shutdown()
    return jsonify({"status": "shutdown success"})

@webserver.route('/api/jobs', methods=['GET'])
def jobs_request():
    job_status = webserver.tasks_runner.get_jobs()
    return jsonify({"status": "done", "jobs": [{"job_id_" + str(job_id) : job_status[job_id]} for job_id in job_status]})

@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs_request():
    if webserver.tasks_runner.is_shutdown_event_set():
        time.sleep(5)
        return 0
    else:
        return jsonify({"num_jobs": str(len(list(filter(lambda pair: pair[1] == 'running', webserver.tasks_runner.get_jobs().items()))))})
        
# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes

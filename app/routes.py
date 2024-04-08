from app import webserver
from flask import request, jsonify

import json

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        data = request.json
        webserver.logger.info(f"{request.method} - {request.url} Received: {data}")

        response = {"message": "Received data successfully", "data": data}

        return jsonify(response)

    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    job_id_status = webserver.tasks_runner.check_job_id(int(job_id))
    if job_id_status is not None:
        webserver.logger.info(f"{request.method} - {request.url}\
                              - Result for job {job_id} requested")
        if job_id_status == 'running':
            return jsonify({"status" : job_id_status})
        else:
            with open(f'results/{job_id}.json', 'r') as result_file:
                result = json.load(result_file)
            return jsonify({"status": job_id_status, "data": result})
    
    webserver.logger.error(f"{request.method} - {request.url} Invalid job ID requested")
    return jsonify({"status": "error", "reason" : "Invalid job_id"})


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    data = request.json
    job_id = webserver.tasks_runner.add_task(data, 'states_mean')

    if job_id is None:
        webserver.logger.error(f"{request.method} - {request.url}\
                               - Server has been shut down, no more jobs accepted")
        return jsonify({"job_id": -1, "reason": "shutting down"})
    
    webserver.logger.info(f"{request.method} - {request.url} - Received: {data}")
    webserver.tasks_runner.update_job_id()
    
    return jsonify({"job_id": job_id})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    data = request.json
    job_id = webserver.tasks_runner.add_task(data, 'state_mean')

    if job_id is None:
        webserver.logger.error(f"{request.method} - {request.url}\
                               - Server has been shut down, no more jobs accepted")
        return jsonify({"job_id": -1, "reason": "shutting down"})
    
    webserver.logger.info(f"{request.method} - {request.url} - Received: {data}")
    webserver.tasks_runner.update_job_id()

    return jsonify({"job_id": job_id})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    data = request.json
    job_id = webserver.tasks_runner.add_task(data, 'best5')

    if job_id is None:
        webserver.logger.error(f"{request.method} - {request.url}\
                               - Server has been shut down, no more jobs accepted")
        return jsonify({"job_id": -1, "reason": "shutting down"})
    
    webserver.logger.info(f"{request.method} - {request.url} - Received: {data}")
    webserver.tasks_runner.update_job_id()

    return jsonify({"job_id": job_id})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    data = request.json
    job_id = webserver.tasks_runner.add_task(data, 'worst5')

    if job_id is None:
        webserver.logger.error(f"{request.method} - {request.url}\
                               - Server has been shut down, no more jobs accepted")
        return jsonify({"job_id": -1, "reason": "shutting down"})
    
    webserver.logger.info(f"{request.method} - {request.url} - Received: {data}")
    webserver.tasks_runner.update_job_id()

    return jsonify({"job_id": job_id})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    data = request.json
    job_id = webserver.tasks_runner.add_task(data, 'global_mean')
    
    if job_id is None:
        webserver.logger.error(f"{request.method} - {request.url}\
                               - Server has been shut down, no more jobs accepted")
        return jsonify({"job_id": -1, "reason": "shutting down"})
    
    webserver.logger.info(f"{request.method} - {request.url} - Received: {data}")
    webserver.tasks_runner.update_job_id()

    return jsonify({"job_id": job_id})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    data = request.json
    job_id = webserver.tasks_runner.add_task(data, 'diff_from_mean')
    
    if job_id is None:
        webserver.logger.error(f"{request.method} - {request.url}\
                               - Server has been shut down, no more jobs accepted")
        return jsonify({"job_id": -1, "reason": "shutting down"})
    
    webserver.logger.info(f"{request.method} - {request.url} - Received: {data}")
    webserver.tasks_runner.update_job_id()

    return jsonify({"job_id": job_id})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    data = request.json
    job_id = webserver.tasks_runner.add_task(data, 'state_diff_from_mean')
    
    if job_id is None:
        webserver.logger.error(f"{request.method} - {request.url}\
                               - Server has been shut down, no more jobs accepted")
        return jsonify({"job_id": -1, "reason": "shutting down"})
    
    webserver.logger.info(f"{request.method} - {request.url} - Received: {data}")
    webserver.tasks_runner.update_job_id()

    return jsonify({"job_id": job_id})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    data = request.json
    job_id = webserver.tasks_runner.add_task(data, 'mean_by_category')
    
    if job_id is None:
        webserver.logger.error(f"{request.method} - {request.url}\
                               - Server has been shut down, no more jobs accepted")
        return jsonify({"job_id": -1, "reason": "shutting down"})
    
    webserver.logger.info(f"{request.method} - {request.url} - Received: {data}")
    webserver.tasks_runner.update_job_id()

    return jsonify({"job_id": job_id})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    data = request.json
    job_id = webserver.tasks_runner.add_task(data, 'state_mean_by_category')
    
    if job_id is None:
        webserver.logger.error(f"{request.method} - {request.url}\
                               - Server has been shut down, no more jobs accepted")
        return jsonify({"job_id": -1, "reason": "shutting down"})
    
    webserver.logger.info(f"{request.method} - {request.url} - Received: {data}")
    webserver.tasks_runner.update_job_id()

    return jsonify({"job_id": job_id})

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown_request():
    if webserver.tasks_runner.is_shutdown_event_set():
        webserver.logger.error(f"{request.method} - {request.url}\
                                - Server shut down already requested")
        return jsonify({"status": "shutdown already requested"})
    
    webserver.logger.info(f"{request.method} - {request.url} - Shutting down the server...")

    webserver.tasks_runner.shutdown()
    return jsonify({"status": "shutdown success"})

@webserver.route('/api/jobs', methods=['GET'])
def jobs_request():
    webserver.logger.info(f"{request.method} - {request.url} - Jobs status requested")
    job_status = webserver.tasks_runner.get_jobs()
    return jsonify({"status": "done", "data": [{"job_id_" + str(job_id) : job_status[job_id]}
                                               for job_id in job_status]})

@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs_request():
    webserver.logger.info(f"{request.method} - {request.url} - Number of running jobs requested")
    return jsonify({"num_jobs": str(len(list(filter(lambda pair: pair[1] == 'running', 
                                                    webserver.tasks_runner.get_jobs().items()))))})
        
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

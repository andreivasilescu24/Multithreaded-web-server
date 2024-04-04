import logging, logging.handlers
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
import time
# from threading import Lock

webserver = Flask(__name__)

# webserver.task_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.logger = logging.getLogger('webserver')
webserver.logger.setLevel(logging.INFO)

logger_handler = logging.handlers.RotatingFileHandler('webserver.log', maxBytes=20000, 
                                                        backupCount=5)

formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
formatter.converter = time.gmtime

logger_handler.setFormatter(formatter)
webserver.logger.addHandler(logger_handler)

webserver.job_counter = 1

webserver.logger.info('Started webserver')
webserver.tasks_runner = ThreadPool(webserver.data_ingestor, webserver.logger)

from app import routes

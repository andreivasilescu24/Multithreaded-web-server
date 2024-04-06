import logging, logging.handlers
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
import time

webserver = Flask(__name__)

webserver.data_ingestor = DataIngestor("nutrition_activity_obesity_usa_subset.csv")

webserver.logger = logging.getLogger(__name__)
webserver.logger.setLevel(logging.INFO)

logger_handler = logging.handlers.RotatingFileHandler('webserver.log', maxBytes=40000, 
                                                        backupCount=5)

formatter = logging.Formatter('%(asctime)s GMT - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
formatter.converter = time.gmtime

logger_handler.setFormatter(formatter)
webserver.logger.addHandler(logger_handler)

webserver.logger.info('Started webserver')
webserver.tasks_runner = ThreadPool(webserver.data_ingestor, webserver.logger)

from app import routes
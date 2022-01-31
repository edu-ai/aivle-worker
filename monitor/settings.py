import logging

import zmq

logger = logging.getLogger("root")
logger.info("Initializing monitor settings. Waiting for worker reply...")
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:55545")

message = socket.recv_pyobj()
API_BASE_URL = message["api_base_url"]
ACCESS_TOKEN = message["access_token"]
FULL_WORKER_NAME = message["full_worker_name"]
QUEUE_NAME = message["queue_name"]
logger.info(f"Monitor settings: {message}")
socket.send_string("OK")

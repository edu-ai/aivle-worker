import argparse

from .settings import update_queue, update_concurrency, update_worker_name, update_zmq_port


def main():
    parser = argparse.ArgumentParser(description="Run aiVLE worker client.")
    parser.add_argument("--queue", type=str, help="aiVLE task queue name, default as 'default'")
    parser.add_argument("--concurrency", type=int, help="maximum number of concurrent evaluation, default as 1")
    parser.add_argument("--worker-name", type=str, help="worker name, default as 'celery'")
    parser.add_argument("--zmq-port", type=int, help="ZMQ port used for communication between monitor, warden and main "
                                                     "worker thread, default as 15921")
    args = parser.parse_args()
    if args.queue:
        update_queue(args.queue)
    if args.concurrency:
        print("updating concurrency")
        update_concurrency(args.concurrency)
    if args.worker_name:
        update_worker_name(args.worker_name)
    if args.zmq_port:
        update_zmq_port(args.zmq_port)
    """
    Ensure you import `entry_point` AFTER initializing the settings.
    Otherwise constants in `setting` might be imported into `entry_point` and other modules as local variables,
    rendering the overriding settings from the command arguments no longer overriding.
    Details: https://docs.python.org/2/reference/simple_stmts.html#the-import-statement
    """
    from .entry_point import start
    start()

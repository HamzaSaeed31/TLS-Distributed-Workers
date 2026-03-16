from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import threading
import queue
import logging
import time
import json
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - COORDINATOR - %(levelname)s - %(message)s'
)

class Coordinator:
    def __init__(self, host, port, worker_configs):
        self.host = host
        self.port = port
        self.workers = []
        self.worker_status = []  # True if worker is healthy
        self.task_queue = queue.Queue()
        self.active_tasks = {}
        self.worker_last_heartbeat = {}
        
        # Initialize server
        self.server = SimpleXMLRPCServer((host, port), allow_none=True, logRequests=True)
        self.server.register_instance(self)
        
        # Initialize workers
        for config in worker_configs:
            worker = ServerProxy(f'http://{config["host"]}:{config["port"]}')
            self.workers.append(worker)
            self.worker_status.append(True)
            self.worker_last_heartbeat[len(self.workers)-1] = time.time()
            
        # Start health monitoring thread
        self.stop_monitoring = False
        self.monitor_thread = threading.Thread(target=self._monitor_workers)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def _monitor_workers(self):
        """Monitor worker health through periodic checks"""
        while not self.stop_monitoring:
            for i, worker in enumerate(self.workers):
                try:
                    # Check if worker is alive
                    worker.matrix_add([[1]], [[1]])  # Simple health check
                    if not self.worker_status[i]:
                        logging.info(f"Worker {i} recovered")
                        self.worker_status[i] = True
                    self.worker_last_heartbeat[i] = time.time()
                except Exception as e:
                    if self.worker_status[i]:
                        logging.error(f"Worker {i} failed: {e}")
                        self.worker_status[i] = False
                    self._handle_worker_failure(i)
            time.sleep(5)  # Check every 5 seconds

    def _handle_worker_failure(self, worker_id):
        """Handle worker failure and reassign tasks"""
        failed_tasks = [
            task_id for task_id, task in self.active_tasks.items()
            if task['worker_id'] == worker_id
        ]
        
        for task_id in failed_tasks:
            task = self.active_tasks[task_id]
            self.task_queue.put(task)
            logging.info(f"Reassigned task {task_id} due to worker failure")

    def get_available_worker(self):
        """Get an available worker with retries"""
        max_attempts = len(self.workers) * 2
        attempts = 0
        
        while attempts < max_attempts:
            for i, status in enumerate(self.worker_status):
                if status:
                    try:
                        # Verify worker is truly available
                        self.workers[i].matrix_add([[1]], [[1]])
                        return i
                    except:
                        self.worker_status[i] = False
            attempts += 1
            time.sleep(1)
            
        raise Exception("No workers available")

    def perform_operation(self, operation, *args):
        """Execute matrix operation with fault tolerance"""
        task = {
            'operation': operation,
            'args': args,
            'attempts': 0,
            'max_attempts': len(self.workers) * 2  # Allow multiple retries
        }
        
        while task['attempts'] < task['max_attempts']:
            try:
                # Get available worker
                worker_id = self.get_available_worker()
                worker = self.workers[worker_id]
                
                # Execute operation
                if operation == 'add':
                    return worker.matrix_add(*args)
                elif operation == 'multiply':
                    return worker.matrix_multiply(*args)
                elif operation == 'transpose':
                    return worker.matrix_transpose(*args)
                else:
                    raise ValueError(f"Unknown operation: {operation}")
                    
            except Exception as e:
                logging.error(f"Operation failed on worker {worker_id}: {e}")
                task['attempts'] += 1
                if task['attempts'] < task['max_attempts']:
                    logging.info(f"Retrying operation (attempt {task['attempts']})")
                    time.sleep(1)  # Wait before retry
                else:
                    raise Exception("All workers failed to process the request")

    def get_system_status(self):
        """Get current system status"""
        return {
            'active_workers': sum(self.worker_status),
            'total_workers': len(self.workers),
            'worker_status': self.worker_status
        }

    def start(self):
        """Start the coordinator server"""
        logging.info(f"Starting coordinator on {self.host}:{self.port}")
        logging.info(f"Managing {len(self.workers)} workers")
        self.server.serve_forever()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python coordinator.py <host> <port> <worker_config_file>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    
    with open(sys.argv[3]) as f:
        worker_configs = json.load(f)
    
    coordinator = Coordinator(host, port, worker_configs)
    try:
        coordinator.start()
    except KeyboardInterrupt:
        coordinator.stop_monitoring = True
        sys.exit(0)
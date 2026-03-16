from xmlrpc.server import SimpleXMLRPCServer
import numpy as np
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - WORKER - %(levelname)s - %(message)s'
)

class MatrixWorker:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
        logging.info(f"Initializing worker on {host}:{port}")
        try:
            self.server = SimpleXMLRPCServer(
                (host, port),
                allow_none=True,
                logRequests=True
            )
            self.server.register_instance(self)
            logging.info("Worker initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize worker: {e}")
            raise

    def matrix_add(self, matrix1, matrix2):
        """Add two matrices"""
        logging.info("Received addition request")
        try:
            result = np.array(matrix1) + np.array(matrix2)
            logging.info("Addition completed successfully")
            return result.tolist()
        except Exception as e:
            logging.error(f"Addition failed: {e}")
            raise

    def matrix_multiply(self, matrix1, matrix2):
        """Multiply two matrices"""
        logging.info("Received multiplication request")
        try:
            result = np.dot(np.array(matrix1), np.array(matrix2))
            logging.info("Multiplication completed successfully")
            return result.tolist()
        except Exception as e:
            logging.error(f"Multiplication failed: {e}")
            raise

    def matrix_transpose(self, matrix):
        """Transpose a matrix"""
        logging.info("Received transpose request")
        try:
            result = np.array(matrix).T
            logging.info("Transpose completed successfully")
            return result.tolist()
        except Exception as e:
            logging.error(f"Transpose failed: {e}")
            raise

    def start(self):
        """Start the worker server"""
        logging.info(f"Starting worker server on {self.host}:{self.port}")
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            logging.info("Shutting down worker")
        except Exception as e:
            logging.error(f"Server error: {e}")
            raise

def main():
    if len(sys.argv) != 3:
        print("Usage: python worker.py <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    
    worker = MatrixWorker(host, port)
    worker.start()

if __name__ == "__main__":
    main()
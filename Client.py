from xmlrpc.client import ServerProxy
import numpy as np
import logging
import sys
import time

# Configure logging with more detail
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for more detailed output
    format='%(asctime)s - CLIENT - %(levelname)s - %(message)s'
)

class MatrixClient:
    def __init__(self, coordinator_host, coordinator_port):
        """Initialize client"""
        self.coordinator_url = f'http://{coordinator_host}:{coordinator_port}'
        logging.info(f"Connecting to coordinator at {self.coordinator_url}")
        self.coordinator = ServerProxy(self.coordinator_url)

    def add_matrices(self, matrix1, matrix2):
        """Add two matrices"""
        logging.info("Requesting matrix addition")
        try:
            result = self.coordinator.perform_operation('add', matrix1.tolist(), matrix2.tolist())
            logging.info("Addition completed successfully")
            return np.array(result)
        except Exception as e:
            logging.error(f"Addition failed: {str(e)}")
            raise

    def multiply_matrices(self, matrix1, matrix2):
        """Multiply two matrices"""
        logging.info("Requesting matrix multiplication")
        try:
            result = self.coordinator.perform_operation('multiply', matrix1.tolist(), matrix2.tolist())
            logging.info("Multiplication completed successfully")
            return np.array(result)
        except Exception as e:
            logging.error(f"Multiplication failed: {str(e)}")
            raise

    def transpose_matrix(self, matrix):
        """Transpose a matrix"""
        logging.info("Requesting matrix transpose")
        try:
            result = self.coordinator.perform_operation('transpose', matrix.tolist())
            logging.info("Transpose completed successfully")
            return np.array(result)
        except Exception as e:
            logging.error(f"Transpose failed: {str(e)}")
            raise

def main():
    if len(sys.argv) != 3:
        print("Usage: python client.py <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    
    logging.info(f"Starting client, connecting to {host}:{port}")
    client = MatrixClient(host, port)

    # Test matrices
    matrix1 = np.array([[1, 2], [3, 4]])
    matrix2 = np.array([[5, 6], [7, 8]])

    logging.info("Starting matrix operations test")
    try:
        # Test addition
        logging.info("\nTesting matrix addition")
        print("\nMatrix 1:")
        print(matrix1)
        print("\nMatrix 2:")
        print(matrix2)
        
        result = client.add_matrices(matrix1, matrix2)
        print("\nAddition Result:")
        print(result)

        # Test multiplication
        logging.info("\nTesting matrix multiplication")
        result = client.multiply_matrices(matrix1, matrix2)
        print("\nMultiplication Result:")
        print(result)

        # Test transpose
        logging.info("\nTesting matrix transpose")
        result = client.transpose_matrix(matrix1)
        print("\nTranspose Result:")
        print(result)

    except Exception as e:
        logging.error(f"Test failed: {str(e)}")
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
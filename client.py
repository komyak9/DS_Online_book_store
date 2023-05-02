from concurrent import futures
import multiprocessing
import random
import threading
import time

import grpc
import book_store_pb2
import book_store_pb2_grpc

class DataStorageServicer(book_store_pb2_grpc.DataStorageServicer):
    def __init__(self, id):
        self.store_id = id
        self.head_node = None
        self.predecessor = None # address
        self.successor = None   # address
        self.books = {}

    def set_chain_dependecies(self, head_node, predecessor, successor):
        self.head_node = head_node
        self.predecessor = predecessor
        self.successor = successor

    # Client sends a request to write.
    # DataStore checks if this particular client has a head node.
    def InitialWriteOperation(self, request, context):
        msg = ""
        if self.predecessor is None:    # In this draft implementation without chain it is always True.
            self.books[request.book_name] = request.book_price
            msg = f"New book is successfully added to {self.store_id} store."
        else:
            channel = grpc.insecure_channel(self.head_node)
            stub = book_store_pb2_grpc.DataStorageStub(channel)
            message = book_store_pb2.CommonWriteOperationRequest(book_name=request.book_name, price=request.price)
            try:
                response = stub.CommonWriteOperation(message)
                msg = response.message
            except grpc.RpcError:
                msg = "Store is not available"
                return book_store_pb2.ListBooksResponse(success=False, message=msg)

        return book_store_pb2.ListBooksResponse(success=True, message=msg)

    def ListBooks(self, request, context):
        msg_string = ""
        if len(self.books) == 0:
            msg_string = "The shop is empty."
        else:
            for key, value in self.books.items():
                msg_string += f"{key}: {value}\n"
        return book_store_pb2.ListBooksResponse(success=True, message=msg_string)

    # Not used in the draft
    def CommonWriteOperation(self, request, context):
        self.books[request.book_name] = request.price

        if self.successor is not None:
            channel = grpc.insecure_channel(self.successor)
            stub = book_store_pb2_grpc.DataStorageStub(channel)
            message = book_store_pb2.CommonWriteOperationRequest(book_name=request.book_name, price=request.price)
            try:
                response = stub.CommonWriteOperation(message)
            except grpc.RpcError:
                print("Server is not available")
        else:
            # When we reached the last process in the chain.
            book_store_pb2.CommonWriteOperationResponse(success=True, message="All chains are updated.")





class BookStoreClient:
    """ Implements store logic """
    def __init__(self, stub, ip_address):
        self.ip_address = ip_address
        self.client_id = None
        self.stub = stub
        # Processes storage of DataStore objects.
        self.processes_addresses = {}

        self.processes_ids = []
        # Ordered processes in a chain.
        self.processes_chain = []   # queue?
        # List of all available commands.
        self.commands = {"Local-store-ps": self.create_local_stores,
                         "Create-chain": self.create_chain,
                         "List-chain": self.list_chain,
                         "Write-operation": self.write_operation,
                         "List-books": self.list_books,
                         "Read-operation": self.read_operation,
                         "Data-status": self.data_status,
                         "Remove-head": self.remove_head,
                         "Restore-head": self.restore_head
                         }

    ######################################
    # Local-store-ps command             #
    ######################################
    def create_local_stores(self, k=1):
        # By default, it creates 1 process.
        # In our implementation, we specify k processes manually.

        # On the server side, it creates ids for the client and the processes.
        # Then, for each DataStore process we create 'servers' and run them in parallel.
        response = self.stub.CreateLocalStores(book_store_pb2.CreateLocalStoresRequest(processes_number=int(k)))
        if response.success:
            self.client_id = response.client_id
            self.processes_ids = response.processes_ids
            print(response.message)
            print(f"Client: {self.client_id}\nProcesses: {self.processes_ids}")

            for process_id, port in zip(response.processes_ids, response.processes_ports):
                self.processes_addresses[process_id] = self.ip_address + ':' + port
                process = multiprocessing.Process(target=run_grpc_server, args=(self.ip_address, port, process_id,))
                print(f"Process {process_id} is running on {self.processes_addresses[process_id]}")
                process.start()
        else:
            print("Something went wrong. Processes are not initialized.")

    ######################################
    # Creates a chain of processes       #
    ######################################
    def create_chain(self):
        # Chain is built out of processes which are placed in a random order.
        # Request to the server?
        pass

    ######################################
    # Removes chain's head               #
    ######################################
    def remove_head(self):
        # Request to the server?
        pass

    ######################################
    # Restored chain's head              #
    ######################################
    def restore_head(self):
        # Request to the server.
        pass

    ######################################
    # List-chain command                 #
    ######################################
    def list_chain(self):
        # Makes a request to the server.
        pass

    ######################################
    # Write-operation command            #
    ######################################
    def write_operation(self, book_name, price):
        # Creates a data item, stores it in the DataStore objects.
        #responsible_process = self.processes_ids[random.randint(0, len(self.processes_ids)-1)]
        responsible_process = self.processes_ids[1] # hard-coded so far
        channel = grpc.insecure_channel(f'{self.processes_addresses[responsible_process]}')
        stub = book_store_pb2_grpc.DataStorageStub(channel)

        message = book_store_pb2.InitialWriteOperationRequest(book_name=book_name, book_price=float(price))
        try:
            response = stub.InitialWriteOperation(message)
            print(response.message)
        except:
            print("New book wasn't added. Something went wrong.")

    ######################################
    # List-books command                 #
    ######################################
    def list_books(self, args):
        # Shows all available books.
        # Data is stored in the DataStore objects.

        # responsible_process = self.processes_ids[random.randint(0, len(self.processes_ids)-1)]
        responsible_process = self.processes_ids[1]
        channel = grpc.insecure_channel(f'{self.processes_addresses[responsible_process]}')
        stub = book_store_pb2_grpc.DataStorageStub(channel)

        message = book_store_pb2.ListBooksRequest()
        response = stub.ListBooks(message)
        print(f"Available books:\n{response.message}")

    ######################################
    # Read-operation command             #
    ######################################
    def read_operation(self, book_name: str):
        # Shows the price of the book.
        # Same data storage issue as discussed in the list-books method.
        pass

    ######################################
    # Data-status command                #
    ######################################
    def data_status(self):
        # Need to check the theory for dirty/clean definitions.
        pass


def run_grpc_server(ip, port, process_id):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    book_store_pb2_grpc.add_DataStorageServicer_to_server(DataStorageServicer(process_id), server)
    server.add_insecure_port(f'{ip}:{port}')
    server.start()
    server.wait_for_termination()


def run_client():
    ip_address = "localhost"
    with grpc.insecure_channel(f'{ip_address}:50051') as channel:
        stub = book_store_pb2_grpc.BookStoreStub(channel)
        client = BookStoreClient(stub, ip_address)
        print("Client is starting...")

        while True:
            # Input a command and it's arguments if there are any.
            command_string = input("Enter a command to execute: ")
            if ' ' in command_string:
                command = command_string.split(' ')[0]
                args = command_string.split(' ')[1:]
            else:
                command = command_string
                args = ['']

            # Extract a command.
            method = client.commands.get(command)

            if method:  # If such command exists.
                method(*args)   # Execute method.
            else:   # If such method doesn't exist.
                print(f"Command {command} does not exist.")


if __name__ == '__main__':
    run_client()
import random
from concurrent import futures
import multiprocessing
import threading
import time

import grpc
import book_store_pb2
import book_store_pb2_grpc

class DataStorageServicer(book_store_pb2_grpc.DataStorageServicer):
    def __init__(self, id, address, predecessor_address, successor_address, head_node_address):
        self.store_id = id
        self.address = address
        self.head_node_address = head_node_address
        self.predecessor_address = predecessor_address
        self.successor_address = successor_address
        self.books = {}

    def ReadFromDataStore(self, request, context):
        """Fetch a book and its price from the data store.
        If this data store is not head, consult the head node
        to check if the current node contains up-to-date info."""
        msg = ""
        success = False
        if request.book_name in self.books:
            success = True
            msg = f"{request.book_name}: {self.books[request.book_name]}"
        else:
            msg = f"Book {request.book_name} is not available in the store."
        return book_store_pb2.ReadFromDataStoreResponse(success=success, message=msg)

    def WriteToDataStore(self, request, context):
        """Respond to client's request for writing a new book to the store.
        Add a new book to the head of the chain and propagate the message to the next node."""
        # If the current node is a head node.
        if self.predecessor_address is None:
            self.books[request.book_name] = request.book_price
            self.propagate_update(
                request.book_name, request.book_price, self.successor_address)
        elif self.successor_address is None:
            # If the current node is a tail node.
            self.books[request.book_name] = request.book_price
        else:
            # If the head node contains the update that is received by the current node,
            # pass the update to the next node in the chain.
            if self.is_price_uptodate(request.book_name, request.book_price):
                self.books[request.book_name] = request.book_price
                self.propagate_update(
                    request.book_name, request.book_price, self.successor_address)
            else:
                # If the current node received updates that are not present in the head node,
                # redirect the request to the head node.
                self.propagate_update(
                    request.book_name, request.book_price, self.head_node_address)
        return book_store_pb2.WriteToDataStoreResponse(success=True, message="Update triggered.")

    def ListBooks(self, request, context):
        # TODO: Check the latest information from the head node.
        msg_string = ""
        if len(self.books) == 0:
            msg_string = "The shop is empty."
        else:
            for key, value in self.books.items():
                msg_string += f"{key}: {value}\n"
        return book_store_pb2.ListBooksResponse(success=True, message=msg_string)

    def propagate_update(self, book_name, book_price, next_node_address):
        """Propagate the update to the next node in the chain."""
        stub = book_store_pb2_grpc.DataStorageStub(
            grpc.insecure_channel(next_node_address))
        try:
            response = stub.WriteToDataStore(
                book_store_pb2.WriteToDataStoreRequest(
                    book_name=book_name, book_price=float(book_price)))
        except grpc.RpcError:
            response = book_store_pb2.WriteToDataStoreResponse(
                success=False, message="Store is not available")
        return response

    def is_price_uptodate(self, book_name, book_price):
        """Check if the current node has the same price as the head node.
        Head node must have the latest price for each book."""
        stub = book_store_pb2_grpc.DataStorageStub(
            grpc.insecure_channel(self.head_node_address))
        response = stub.ReadFromDataStore(
            book_store_pb2.ReadFromDataStoreRequest(book_name=book_name))
        return True if str(book_price) in response.message else False


class BookStoreClient:
    """ Implements store logic """
    def __init__(self, stub, ip_address):
        self.ip_address = ip_address
        self.client_id = None
        self.stub = stub
        # Dictionary for holding addresses of the data stores.
        self.processes_addresses = {}
        # Chain-related info
        self.processes_ids = []
        self.processes_ports = []
        self.is_chain_created = False
        # Container for a chain of processes.
        self.processes_chain = []
        self.commands = {
            "Local-store-ps": self.create_local_stores,
            "Create-chain": self.create_chain,
            "List-chain": self.list_chain,
            "Write-operation": self.write,
            "List-books": self.list_books,
            "Read-operation": self.read,
            "Data-status": self.data_status,
            "Remove-head": self.remove_head,
            "Restore-head": self.restore_head
         }

    def create_local_stores(self, k=1):
        """Local-store-ps command. Creates k processes on the client side."""
        # On the server side, it creates ids for the client and the processes.
        response = self.stub.CreateLocalStores(book_store_pb2.CreateLocalStoresRequest(processes_number=int(k),
                                                                                       ip_address = self.ip_address))
        if response.success:
            self.client_id = response.client_id
            self.processes_ids = response.processes_ids

            print(response.message)
            print(f"Client: {self.client_id}\nProcesses: {self.processes_ids}")
        else:
            print("Something went wrong. Processes are not initialized.")

    def create_chain(self, args):
        """Creates a chain of processes. Server creates a chain with all the processes
         and assigns ports for each DataStore. For each client's DataStore process we
         create 'servers' and run them in parallel."""
        response = self.stub.CreateChain(
            book_store_pb2.CreateChainRequest(client_id=self.client_id))
        if response.success:
            self.is_chain_created = True
            print(f"{response.message}")

            self.initiate_process_creation(response)

        else:
            print(f"Chain wasn't created: {response.message}")

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

    def list_chain(self, args):
        """Send a request to show the chain of processes. Print the response."""
        # TODO: Make the output prettier.
        print(self.stub.ListChain(book_store_pb2.ListChainRequest()))

    def write(self, book_name, price):
        """Write-operation command. Writes a new book to the chain."""
        if not self.is_chain_created:
            print("To call this function, a chain must be created first.")
            return

        # responsible_process = self.processes_ids[0]  # hard-coded so far
        responsible_process = self.processes_ids[random.randint(0, len(self.processes_ids)-1)]
        print(f"Writing to process {responsible_process}")

        stub = book_store_pb2_grpc.DataStorageStub(
            grpc.insecure_channel(f'{self.processes_addresses[responsible_process]}'))

        try:
            response = stub.WriteToDataStore(
                book_store_pb2.WriteToDataStoreRequest(
                    book_name=book_name, book_price=float(price)))
            print(response.message)
        except Exception as e:
            print("New book wasn't added. Something went wrong.")
            print(e)

    def read(self, book_name: str):
        """Read-operation command. Reads a book from the chain. Sends a request to
        a DataStore process and prints the response."""
        if not self.is_chain_created:
            print("To call this function, a chain must be created first.")
            return

        # responsible_process = self.processes_ids[1]  # hard-coded so far
        responsible_process = self.processes_ids[random.randint(0, len(self.processes_ids)-1)]
        print(f"Reading from process {responsible_process}")
        channel = grpc.insecure_channel(f'{self.processes_addresses[responsible_process]}')
        stub = book_store_pb2_grpc.DataStorageStub(channel)

        try:
            response = stub.ReadFromDataStore(
                book_store_pb2.ReadFromDataStoreRequest(book_name=book_name))
            print(response.message)
        except:
            print("Unable to read the book. Something went wrong.")

    ######################################
    # List-books command                 #
    ######################################
    def list_books(self, args):
        # Shows all available books.
        # Data is stored in the DataStore objects.
        if not self.is_chain_created:
            print(f"To call this function, a chain must be created.")
            return

        responsible_process = self.processes_ids[random.randint(0, len(self.processes_ids)-1)]
        # responsible_process = self.processes_ids[1]
        print(f"Listing books from process {responsible_process}")
        channel = grpc.insecure_channel(f'{self.processes_addresses[responsible_process]}')
        stub = book_store_pb2_grpc.DataStorageStub(channel)

        message = book_store_pb2.ListBooksRequest()
        response = stub.ListBooks(message)
        print(f"Available books:\n{response.message}")

    ######################################
    # Data-status command                #
    ######################################
    def data_status(self):
        # Need to check the theory for dirty/clean definitions.
        pass


    def check_chain_created(self):
        while not self.is_chain_created:
            if self.client_id is None:
                time.sleep(10)
                continue

            message = book_store_pb2.CheckChainRequest(client_id=self.client_id)
            response = self.stub.CheckChain(message)

            if not response.is_chain_created:
                time.sleep(10)
                continue
            else:
                self.is_chain_created = True
                self.initiate_process_creation(response)

    def initiate_process_creation(self, response):
        head_node_address = response.head_node_address
        processes_sucs_preds = dict(response.processes_sucs_preds)
        self.processes_addresses = dict(response.processes_addresses)

        for process_id in self.processes_ids:
            address = self.processes_addresses.get(process_id)
            predecessor_id = processes_sucs_preds[process_id].split(',')[0]
            successor_id = processes_sucs_preds[process_id].split(',')[1]
            if predecessor_id == 'None':
                predecessor = None
            else:
                predecessor = self.processes_addresses.get(predecessor_id)
            if successor_id == 'None':
                successor = None
            else:
                successor = self.processes_addresses.get(successor_id)

            #print(f"\n-- {predecessor_id} -- {process_id} -- {successor_id} --")
            #print(f"-- {predecessor} -- {address} -- {successor} --\n")
            process = multiprocessing.Process(target=run_grpc_server,
                                              args=(address, process_id, predecessor, successor,
                                                    head_node_address,))
            print(f"Process {process_id} is running on {address}")
            process.start()

    def remove_head(self):
        """Initiate remove head on its local store. The local store should
        know who is the head so it sends a request to the head to remove itself
        and propagate that info further."""
        pass


def run_grpc_server(address, process_id, predecessor_address,
                    successor_address, head_node_address):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    book_store_pb2_grpc.add_DataStorageServicer_to_server(
        DataStorageServicer(
            process_id, address, predecessor_address,
            successor_address, head_node_address),
        server)
    server.add_insecure_port(f'{address}')
    server.start()
    server.wait_for_termination()


def run_client():
    ip_address = "localhost"
    with grpc.insecure_channel(f'{ip_address}:50051') as channel:
        stub = book_store_pb2_grpc.BookStoreStub(channel)
        client = BookStoreClient(stub, ip_address)
        print("Client is starting...")

        # Pinging server to figure out if a chain exists
        my_thread = threading.Thread(target=client.check_chain_created)
        my_thread.start()

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